"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
SCHEMAS: ML DEMAND & REVENUE PREDICTION
================================================================================
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PredictionRequest(BaseModel):
    category: str = Field(default="Set", description="Apparel category (e.g., Set, Kurta, Western Dress, Top, Saree)")
    forecast_days: int = Field(default=14, ge=1, le=60, description="Forecast horizon in days (1 to 60)")
    promotion_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Custom promotion discount scenario ratio")
    b2b_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Custom B2B share scenario ratio")


class DailyForecastItem(BaseModel):
    date: str
    day_of_week: str
    is_weekend: bool
    predicted_revenue_inr: float
    predicted_unit_demand: int
    lower_bound_inr: float
    upper_bound_inr: float


class ForecastKpis(BaseModel):
    total_predicted_revenue_inr: float
    total_predicted_unit_demand: int
    daily_average_revenue_inr: float
    avg_selling_price_inr: float


class ModelInfo(BaseModel):
    model_name: str
    algorithm: str
    target_metric: str
    feature_count: int
    features_used: List[str]
    training_r2_score: float
    testing_r2_score: float
    testing_mae_inr: float


class HistoricalPoint(BaseModel):
    date: str
    actual_revenue: float
    actual_units: int


class PredictionResponse(BaseModel):
    status: str
    category: str
    forecast_horizon_days: int
    forecast_start_date: str
    forecast_end_date: str
    kpis: ForecastKpis
    daily_forecast: List[DailyForecastItem]
    recent_history: List[HistoricalPoint]
    model_info: ModelInfo
    interpretation: str
    disclaimer: str
