"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
API ROUTES: ANALYTICS & DASHBOARD KPIS
================================================================================
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from backend.services.analytics_service import AnalyticsService
from backend.schemas.analytics import (
    FilterParams,
    KpiResponse,
    SalesTrendResponse,
    CategoryResponse,
    TopProductsResponse,
    GeographyResponse,
    OrderStatusResponse,
    CourierStatusResponse,
    FulfilmentResponse,
    SalesChannelResponse,
    FilterOptionsResponse,
)

router = APIRouter(prefix="/api", tags=["Analytics & KPIs"])


def parse_filters(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Category filter or 'ALL'"),
    state: Optional[str] = Query(None, description="State filter or 'ALL'"),
    status: Optional[str] = Query(None, description="Status filter or 'ALL'"),
    fulfilment: Optional[str] = Query(None, description="Fulfilment method or 'ALL'"),
    sales_channel: Optional[str] = Query(None, description="Sales channel or 'ALL'"),
) -> FilterParams:
    return FilterParams(
        start_date=start_date,
        end_date=end_date,
        category=category,
        state=state,
        status=status,
        fulfilment=fulfilment,
        sales_channel=sales_channel,
    )


@router.get("/kpis", response_model=KpiResponse, summary="Get Executive Dashboard KPIs")
def get_dashboard_kpis(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_kpis(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate KPIs: {str(e)}")


@router.get("/sales-trend", response_model=SalesTrendResponse, summary="Get Sales Revenue & Order Trends")
def get_sales_trend(
    granularity: str = Query("monthly", pattern="^(monthly|daily)$", description="Trend granularity ('monthly' or 'daily')"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_sales_trend(filters, granularity=granularity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sales trend: {str(e)}")


@router.get("/categories", response_model=CategoryResponse, summary="Get Category-Level Performance")
def get_categories(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_categories(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")


@router.get("/top-products", response_model=TopProductsResponse, summary="Get Top Performing Styles & SKUs")
def get_top_products(
    limit: int = Query(10, ge=1, le=50),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_top_products(filters, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top products: {str(e)}")


@router.get("/geography", response_model=GeographyResponse, summary="Get Regional & State Sales Distribution")
def get_geography(
    state_limit: int = Query(15, ge=1, le=50),
    city_limit: int = Query(15, ge=1, le=50),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_geography(filters, state_limit=state_limit, city_limit=city_limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch geography insights: {str(e)}")


@router.get("/order-status", response_model=OrderStatusResponse, summary="Get Order Status Distribution")
def get_order_status(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_order_status(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch order statuses: {str(e)}")


@router.get("/courier-status", response_model=CourierStatusResponse, summary="Get Courier Status Distribution")
def get_courier_status(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_courier_status(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch courier statuses: {str(e)}")


@router.get("/fulfilment", response_model=FulfilmentResponse, summary="Get Fulfilment Channel Performance")
def get_fulfilment(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_fulfilment(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch fulfilment metrics: {str(e)}")


@router.get("/sales-channel", response_model=SalesChannelResponse, summary="Get Platform Sales Channel Performance")
def get_sales_channel(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    fulfilment: Optional[str] = Query(None),
    sales_channel: Optional[str] = Query(None),
):
    try:
        filters = parse_filters(start_date, end_date, category, state, status, fulfilment, sales_channel)
        return AnalyticsService.get_sales_channel(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sales channels: {str(e)}")


@router.get("/filter-options", response_model=FilterOptionsResponse, summary="Get Available Filter Dropdown Options")
def get_filter_options():
    try:
        return AnalyticsService.get_filter_options()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch filter options: {str(e)}")
