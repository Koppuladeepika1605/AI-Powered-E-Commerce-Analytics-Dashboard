"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
SERVICE: ANALYTICS & BUSINESS KPI COMPUTATION
================================================================================
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Tuple
from backend.database.connection import db_manager
from backend.schemas.analytics import (
    FilterParams,
    KpiResponse,
    SalesTrendResponse,
    SalesTrendItem,
    CategoryResponse,
    CategoryPerformanceItem,
    TopProductsResponse,
    TopProductItem,
    GeographyResponse,
    StateSalesItem,
    CitySalesItem,
    OrderStatusResponse,
    OrderStatusItem,
    CourierStatusResponse,
    CourierStatusItem,
    FulfilmentResponse,
    FulfilmentItem,
    SalesChannelResponse,
    SalesChannelItem,
    FilterOptionsResponse,
)


class AnalyticsService:

    @staticmethod
    def _build_where_clause(filters: FilterParams) -> Tuple[str, dict]:
        conditions = []
        params = {}

        if filters.start_date:
            conditions.append("order_date >= :start_date")
            params["start_date"] = filters.start_date
        if filters.end_date:
            conditions.append("order_date <= :end_date")
            params["end_date"] = filters.end_date
        if filters.category and filters.category != "ALL":
            conditions.append("LOWER(category) = LOWER(:category)")
            params["category"] = filters.category
        if filters.state and filters.state != "ALL":
            conditions.append("LOWER(ship_state) = LOWER(:state)")
            params["state"] = filters.state
        if filters.status and filters.status != "ALL":
            conditions.append("LOWER(status) = LOWER(:status)")
            params["status"] = filters.status
        if filters.fulfilment and filters.fulfilment != "ALL":
            conditions.append("LOWER(fulfilment) = LOWER(:fulfilment)")
            params["fulfilment"] = filters.fulfilment
        if filters.sales_channel and filters.sales_channel != "ALL":
            conditions.append("LOWER(sales_channel) = LOWER(:sales_channel)")
            params["sales_channel"] = filters.sales_channel

        where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        return where_sql, params

    @classmethod
    def get_kpis(cls, filters: FilterParams) -> KpiResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            COUNT(DISTINCT order_id)                                AS total_orders,
            COUNT(*)                                                AS total_lines,
            COALESCE(SUM(qty), 0)                                   AS total_units,
            COALESCE(SUM(gross_amount), 0.0)                        AS total_gross,
            COALESCE(SUM(realized_revenue), 0.0)                    AS total_realized,
            COALESCE(SUM(CASE WHEN is_cancelled = 1 OR is_cancelled = TRUE THEN 1.0 ELSE 0 END), 0.0) AS cancelled_lines,
            COALESCE(SUM(CASE WHEN is_returned = 1 OR is_returned = TRUE THEN 1.0 ELSE 0 END), 0.0)   AS returned_lines,
            COALESCE(SUM(CASE WHEN is_b2b = 1 OR is_b2b = TRUE THEN realized_revenue ELSE 0 END), 0.0) AS b2b_realized,
            COALESCE(SUM(CASE WHEN has_promotion = 1 OR has_promotion = TRUE THEN 1.0 ELSE 0 END), 0.0) AS promo_lines
        FROM amazon_sales
        {where_sql};
        """
        df = db_manager.execute_query_df(query, params)

        if df.empty or df.iloc[0]["total_lines"] == 0:
            return KpiResponse(
                total_sales_gross=0.0,
                total_sales_realized=0.0,
                total_orders=0,
                total_units_sold=0,
                average_order_value=0.0,
                cancellation_rate_pct=0.0,
                return_rate_pct=0.0,
                realization_rate_pct=0.0,
                lost_revenue_inr=0.0,
                b2b_sales_pct=0.0,
                promo_usage_pct=0.0,
            )

        row = df.iloc[0]
        total_orders = int(row["total_orders"])
        total_lines = int(row["total_lines"])
        total_units = int(row["total_units"])
        gross_sales = float(row["total_gross"])
        realized_sales = float(row["total_realized"])
        lost_rev = max(0.0, gross_sales - realized_sales)

        aov = (realized_sales / total_orders) if total_orders > 0 else 0.0
        cancel_pct = (row["cancelled_lines"] / total_lines * 100) if total_lines > 0 else 0.0
        return_pct = (row["returned_lines"] / total_lines * 100) if total_lines > 0 else 0.0
        realiz_pct = (realized_sales / gross_sales * 100) if gross_sales > 0 else 0.0
        b2b_pct = (row["b2b_realized"] / realized_sales * 100) if realized_sales > 0 else 0.0
        promo_pct = (row["promo_lines"] / total_lines * 100) if total_lines > 0 else 0.0

        return KpiResponse(
            total_sales_gross=round(gross_sales, 2),
            total_sales_realized=round(realized_sales, 2),
            total_orders=total_orders,
            total_units_sold=total_units,
            average_order_value=round(aov, 2),
            cancellation_rate_pct=round(cancel_pct, 2),
            return_rate_pct=round(return_pct, 2),
            realization_rate_pct=round(realiz_pct, 2),
            lost_revenue_inr=round(lost_rev, 2),
            b2b_sales_pct=round(b2b_pct, 2),
            promo_usage_pct=round(promo_pct, 2),
        )

    @classmethod
    def get_sales_trend(cls, filters: FilterParams, granularity: str = "monthly") -> SalesTrendResponse:
        where_sql, params = cls._build_where_clause(filters)

        if granularity == "daily":
            query = f"""
            SELECT 
                order_date AS period,
                COUNT(DISTINCT order_id) AS order_count,
                COALESCE(SUM(qty), 0) AS units_sold,
                COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
                COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
            FROM amazon_sales
            {where_sql}
            GROUP BY order_date
            ORDER BY order_date ASC;
            """
        else:
            query = f"""
            SELECT 
                month_name AS period,
                order_year,
                order_month,
                COUNT(DISTINCT order_id) AS order_count,
                COALESCE(SUM(qty), 0) AS units_sold,
                COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
                COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
            FROM amazon_sales
            {where_sql}
            GROUP BY order_year, order_month, month_name
            ORDER BY order_year ASC, order_month ASC;
            """

        df = db_manager.execute_query_df(query, params)
        items = []
        prev_rev = None

        for _, row in df.iterrows():
            curr_rev = float(row["realized_revenue"])
            growth = None
            if prev_rev is not None and prev_rev > 0:
                growth = round(((curr_rev - prev_rev) / prev_rev) * 100, 2)
            prev_rev = curr_rev

            items.append(
                SalesTrendItem(
                    period=str(row["period"]),
                    order_count=int(row["order_count"]),
                    units_sold=int(row["units_sold"]),
                    gross_amount=round(float(row["gross_amount"]), 2),
                    realized_revenue=round(curr_rev, 2),
                    growth_pct=growth,
                )
            )

        return SalesTrendResponse(granularity=granularity, data=items)

    @classmethod
    def get_categories(cls, filters: FilterParams) -> CategoryResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            category,
            COUNT(*) AS total_transactions,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue,
            COALESCE(SUM(CASE WHEN is_cancelled = 1 OR is_cancelled = TRUE THEN 1.0 ELSE 0 END), 0.0) AS cancel_lines
        FROM amazon_sales
        {where_sql}
        GROUP BY category
        ORDER BY realized_revenue DESC;
        """
        df = db_manager.execute_query_df(query, params)
        total_rev = df["realized_revenue"].sum() if not df.empty else 0.0

        items = []
        for _, row in df.iterrows():
            gross = float(row["gross_amount"])
            realized = float(row["realized_revenue"])
            trans = int(row["total_transactions"])
            cancels = float(row["cancel_lines"])

            share_pct = (realized / total_rev * 100) if total_rev > 0 else 0.0
            realiz_pct = (realized / gross * 100) if gross > 0 else 0.0
            cancel_pct = (cancels / trans * 100) if trans > 0 else 0.0

            items.append(
                CategoryPerformanceItem(
                    category=str(row["category"]),
                    total_transactions=trans,
                    total_quantity=int(row["total_quantity"]),
                    gross_amount=round(gross, 2),
                    realized_revenue=round(realized, 2),
                    revenue_share_pct=round(share_pct, 2),
                    realization_rate_pct=round(realiz_pct, 2),
                    cancellation_rate_pct=round(cancel_pct, 2),
                )
            )

        return CategoryResponse(data=items)

    @classmethod
    def get_top_products(cls, filters: FilterParams, limit: int = 10) -> TopProductsResponse:
        where_sql, params = cls._build_where_clause(filters)

        # Top Styles
        style_query = f"""
        SELECT 
            style,
            category,
            COUNT(*) AS total_orders,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {where_sql}
        GROUP BY style, category
        ORDER BY realized_revenue DESC
        LIMIT {limit};
        """
        style_df = db_manager.execute_query_df(style_query, params)

        top_styles = []
        for _, row in style_df.iterrows():
            gross = float(row["gross_amount"])
            realized = float(row["realized_revenue"])
            realiz_pct = (realized / gross * 100) if gross > 0 else 0.0
            top_styles.append(
                TopProductItem(
                    style=str(row["style"]),
                    category=str(row["category"]),
                    total_orders=int(row["total_orders"]),
                    total_quantity=int(row["total_quantity"]),
                    gross_amount=round(gross, 2),
                    realized_revenue=round(realized, 2),
                    realization_rate_pct=round(realiz_pct, 2),
                )
            )

        # Top SKUs
        sku_query = f"""
        SELECT 
            sku,
            style,
            category,
            COUNT(*) AS total_orders,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {where_sql}
        GROUP BY sku, style, category
        ORDER BY realized_revenue DESC
        LIMIT {limit};
        """
        sku_df = db_manager.execute_query_df(sku_query, params)

        top_skus = []
        for _, row in sku_df.iterrows():
            gross = float(row["gross_amount"])
            realized = float(row["realized_revenue"])
            realiz_pct = (realized / gross * 100) if gross > 0 else 0.0
            top_skus.append(
                TopProductItem(
                    sku=str(row["sku"]),
                    style=str(row["style"]),
                    category=str(row["category"]),
                    total_orders=int(row["total_orders"]),
                    total_quantity=int(row["total_quantity"]),
                    gross_amount=round(gross, 2),
                    realized_revenue=round(realized, 2),
                    realization_rate_pct=round(realiz_pct, 2),
                )
            )

        return TopProductsResponse(top_styles=top_styles, top_skus=top_skus)

    @classmethod
    def get_geography(cls, filters: FilterParams, state_limit: int = 15, city_limit: int = 15) -> GeographyResponse:
        where_sql, params = cls._build_where_clause(filters)

        # State aggregations
        state_query = f"""
        SELECT 
            ship_state,
            COUNT(DISTINCT order_id) AS total_orders,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue,
            COUNT(*) AS total_lines,
            COALESCE(SUM(CASE WHEN is_cancelled = 1 OR is_cancelled = TRUE THEN 1.0 ELSE 0 END), 0.0) AS cancel_lines
        FROM amazon_sales
        {where_sql}
        GROUP BY ship_state
        ORDER BY realized_revenue DESC
        LIMIT {state_limit};
        """
        state_df = db_manager.execute_query_df(state_query, params)
        total_rev = state_df["realized_revenue"].sum() if not state_df.empty else 0.0

        top_states = []
        for _, row in state_df.iterrows():
            realized = float(row["realized_revenue"])
            lines = int(row["total_lines"])
            cancels = float(row["cancel_lines"])
            share_pct = (realized / total_rev * 100) if total_rev > 0 else 0.0
            cancel_pct = (cancels / lines * 100) if lines > 0 else 0.0

            top_states.append(
                StateSalesItem(
                    state=str(row["ship_state"]),
                    total_orders=int(row["total_orders"]),
                    total_quantity=int(row["total_quantity"]),
                    realized_revenue=round(realized, 2),
                    revenue_share_pct=round(share_pct, 2),
                    cancellation_rate_pct=round(cancel_pct, 2),
                )
            )

        # City aggregations (exclude unknown)
        city_clause = (where_sql + " AND " if where_sql else "WHERE ") + "ship_city != 'Unknown/Not Provided'"
        city_query = f"""
        SELECT 
            ship_city,
            ship_state,
            COUNT(DISTINCT order_id) AS total_orders,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {city_clause}
        GROUP BY ship_city, ship_state
        ORDER BY realized_revenue DESC
        LIMIT {city_limit};
        """
        city_df = db_manager.execute_query_df(city_query, params)

        top_cities = []
        for _, row in city_df.iterrows():
            top_cities.append(
                CitySalesItem(
                    city=str(row["ship_city"]),
                    state=str(row["ship_state"]),
                    total_orders=int(row["total_orders"]),
                    realized_revenue=round(float(row["realized_revenue"]), 2),
                )
            )

        return GeographyResponse(top_states=top_states, top_cities=top_cities)

    @classmethod
    def get_order_status(cls, filters: FilterParams) -> OrderStatusResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            status,
            COUNT(*) AS order_count,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {where_sql}
        GROUP BY status
        ORDER BY order_count DESC;
        """
        df = db_manager.execute_query_df(query, params)
        total_records = df["order_count"].sum() if not df.empty else 0

        items = []
        for _, row in df.iterrows():
            cnt = int(row["order_count"])
            share_pct = (cnt / total_records * 100) if total_records > 0 else 0.0
            items.append(
                OrderStatusItem(
                    status=str(row["status"]),
                    order_count=cnt,
                    share_pct=round(share_pct, 2),
                    total_quantity=int(row["total_quantity"]),
                    realized_revenue=round(float(row["realized_revenue"]), 2),
                )
            )

        return OrderStatusResponse(data=items)

    @classmethod
    def get_courier_status(cls, filters: FilterParams) -> CourierStatusResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            courier_status,
            COUNT(*) AS order_count,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {where_sql}
        GROUP BY courier_status
        ORDER BY order_count DESC;
        """
        df = db_manager.execute_query_df(query, params)
        total_records = df["order_count"].sum() if not df.empty else 0

        items = []
        for _, row in df.iterrows():
            cnt = int(row["order_count"])
            share_pct = (cnt / total_records * 100) if total_records > 0 else 0.0
            items.append(
                CourierStatusItem(
                    courier_status=str(row["courier_status"]),
                    order_count=cnt,
                    share_pct=round(share_pct, 2),
                    total_quantity=int(row["total_quantity"]),
                    realized_revenue=round(float(row["realized_revenue"]), 2),
                )
            )

        return CourierStatusResponse(data=items)

    @classmethod
    def get_fulfilment(cls, filters: FilterParams) -> FulfilmentResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            fulfilment,
            fulfilled_by,
            COUNT(*) AS order_lines,
            COALESCE(SUM(qty), 0) AS total_quantity,
            COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue,
            COALESCE(SUM(CASE WHEN is_cancelled = 1 OR is_cancelled = TRUE THEN 1.0 ELSE 0 END), 0.0) AS cancel_lines
        FROM amazon_sales
        {where_sql}
        GROUP BY fulfilment, fulfilled_by
        ORDER BY order_lines DESC;
        """
        df = db_manager.execute_query_df(query, params)
        total_lines = df["order_lines"].sum() if not df.empty else 0

        items = []
        for _, row in df.iterrows():
            lines = int(row["order_lines"])
            gross = float(row["gross_amount"])
            realized = float(row["realized_revenue"])
            cancels = float(row["cancel_lines"])

            share_pct = (lines / total_lines * 100) if total_lines > 0 else 0.0
            realiz_pct = (realized / gross * 100) if gross > 0 else 0.0
            cancel_pct = (cancels / lines * 100) if lines > 0 else 0.0

            items.append(
                FulfilmentItem(
                    fulfilment=str(row["fulfilment"]),
                    fulfilled_by=str(row["fulfilled_by"]),
                    order_lines=lines,
                    volume_share_pct=round(share_pct, 2),
                    total_quantity=int(row["total_quantity"]),
                    gross_amount=round(gross, 2),
                    realized_revenue=round(realized, 2),
                    realization_rate_pct=round(realiz_pct, 2),
                    cancellation_rate_pct=round(cancel_pct, 2),
                )
            )

        return FulfilmentResponse(data=items)

    @classmethod
    def get_sales_channel(cls, filters: FilterParams) -> SalesChannelResponse:
        where_sql, params = cls._build_where_clause(filters)

        query = f"""
        SELECT 
            sales_channel,
            COUNT(*) AS total_records,
            COALESCE(SUM(qty), 0) AS total_units,
            COALESCE(SUM(gross_amount), 0.0) AS gross_amount,
            COALESCE(SUM(realized_revenue), 0.0) AS realized_revenue
        FROM amazon_sales
        {where_sql}
        GROUP BY sales_channel
        ORDER BY total_records DESC;
        """
        df = db_manager.execute_query_df(query, params)
        total_recs = df["total_records"].sum() if not df.empty else 0

        items = []
        for _, row in df.iterrows():
            cnt = int(row["total_records"])
            gross = float(row["gross_amount"])
            realized = float(row["realized_revenue"])
            share_pct = (cnt / total_recs * 100) if total_recs > 0 else 0.0
            realiz_pct = (realized / gross * 100) if gross > 0 else 0.0

            items.append(
                SalesChannelItem(
                    sales_channel=str(row["sales_channel"]),
                    total_records=cnt,
                    channel_share_pct=round(share_pct, 2),
                    total_units=int(row["total_units"]),
                    gross_amount=round(gross, 2),
                    realized_revenue=round(realized, 2),
                    realization_rate_pct=round(realiz_pct, 2),
                )
            )

        return SalesChannelResponse(data=items)

    @classmethod
    def get_filter_options(cls) -> FilterOptionsResponse:
        categories_query = "SELECT DISTINCT category FROM amazon_sales ORDER BY category ASC;"
        states_query = "SELECT DISTINCT ship_state FROM amazon_sales WHERE ship_state != 'Unknown/Not Provided' ORDER BY ship_state ASC;"
        statuses_query = "SELECT DISTINCT status FROM amazon_sales ORDER BY status ASC;"
        fulfilment_query = "SELECT DISTINCT fulfilment FROM amazon_sales ORDER BY fulfilment ASC;"
        channels_query = "SELECT DISTINCT sales_channel FROM amazon_sales ORDER BY sales_channel ASC;"
        date_query = "SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date FROM amazon_sales;"

        cats = db_manager.execute_query_df(categories_query)["category"].tolist()
        states = db_manager.execute_query_df(states_query)["ship_state"].tolist()
        statuses = db_manager.execute_query_df(statuses_query)["status"].tolist()
        fulfilments = db_manager.execute_query_df(fulfilment_query)["fulfilment"].tolist()
        channels = db_manager.execute_query_df(channels_query)["sales_channel"].tolist()
        dates = db_manager.execute_query_df(date_query).iloc[0]

        return FilterOptionsResponse(
            categories=["ALL"] + cats,
            states=["ALL"] + states,
            statuses=["ALL"] + statuses,
            fulfilment_types=["ALL"] + fulfilments,
            sales_channels=["ALL"] + channels,
            date_range={"min_date": str(dates["min_date"]), "max_date": str(dates["max_date"])},
        )
