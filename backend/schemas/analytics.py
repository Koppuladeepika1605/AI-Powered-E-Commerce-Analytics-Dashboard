"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
SCHEMAS: ANALYTICS & DASHBOARD KPIS
================================================================================
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class FilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    fulfilment: Optional[str] = None
    sales_channel: Optional[str] = None


class KpiResponse(BaseModel):
    total_sales_gross: float = Field(..., description="Total gross listed sales in INR")
    total_sales_realized: float = Field(..., description="Total realized net revenue in INR")
    total_orders: int = Field(..., description="Total distinct customer orders")
    total_units_sold: int = Field(..., description="Total product units sold")
    average_order_value: float = Field(..., description="Average realized order value (AOV)")
    cancellation_rate_pct: float = Field(..., description="Percentage of cancelled transactions")
    return_rate_pct: float = Field(..., description="Percentage of returned transactions")
    realization_rate_pct: float = Field(..., description="Percentage of gross revenue realized")
    lost_revenue_inr: float = Field(..., description="Unrealized revenue from cancellations/returns")
    b2b_sales_pct: float = Field(..., description="Percentage of sales from B2B wholesale buyers")
    promo_usage_pct: float = Field(..., description="Percentage of orders using coupon/promotions")


class SalesTrendItem(BaseModel):
    period: str
    order_count: int
    units_sold: int
    gross_amount: float
    realized_revenue: float
    growth_pct: Optional[float] = None


class SalesTrendResponse(BaseModel):
    granularity: str
    data: List[SalesTrendItem]


class CategoryPerformanceItem(BaseModel):
    category: str
    total_transactions: int
    total_quantity: int
    gross_amount: float
    realized_revenue: float
    revenue_share_pct: float
    realization_rate_pct: float
    cancellation_rate_pct: float


class CategoryResponse(BaseModel):
    data: List[CategoryPerformanceItem]


class TopProductItem(BaseModel):
    style: Optional[str] = None
    sku: Optional[str] = None
    category: str
    total_orders: int
    total_quantity: int
    gross_amount: float
    realized_revenue: float
    realization_rate_pct: float


class TopProductsResponse(BaseModel):
    top_styles: List[TopProductItem]
    top_skus: List[TopProductItem]


class StateSalesItem(BaseModel):
    state: str
    total_orders: int
    total_quantity: int
    realized_revenue: float
    revenue_share_pct: float
    cancellation_rate_pct: float


class CitySalesItem(BaseModel):
    city: str
    state: str
    total_orders: int
    realized_revenue: float


class GeographyResponse(BaseModel):
    top_states: List[StateSalesItem]
    top_cities: List[CitySalesItem]


class OrderStatusItem(BaseModel):
    status: str
    order_count: int
    share_pct: float
    total_quantity: int
    realized_revenue: float


class OrderStatusResponse(BaseModel):
    data: List[OrderStatusItem]


class CourierStatusItem(BaseModel):
    courier_status: str
    order_count: int
    share_pct: float
    total_quantity: int
    realized_revenue: float


class CourierStatusResponse(BaseModel):
    data: List[CourierStatusItem]


class FulfilmentItem(BaseModel):
    fulfilment: str
    fulfilled_by: str
    order_lines: int
    volume_share_pct: float
    total_quantity: int
    gross_amount: float
    realized_revenue: float
    realization_rate_pct: float
    cancellation_rate_pct: float


class FulfilmentResponse(BaseModel):
    data: List[FulfilmentItem]


class SalesChannelItem(BaseModel):
    sales_channel: str
    total_records: int
    channel_share_pct: float
    total_units: int
    gross_amount: float
    realized_revenue: float
    realization_rate_pct: float


class SalesChannelResponse(BaseModel):
    data: List[SalesChannelItem]


class FilterOptionsResponse(BaseModel):
    categories: List[str]
    states: List[str]
    statuses: List[str]
    fulfilment_types: List[str]
    sales_channels: List[str]
    date_range: Dict[str, str]
