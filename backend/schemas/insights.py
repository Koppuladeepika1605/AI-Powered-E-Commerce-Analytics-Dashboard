"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
SCHEMAS: AI BUSINESS INSIGHTS & ANOMALY DETECTION
================================================================================
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class InsightItem(BaseModel):
    id: str
    category: str = Field(..., description="E.g., 'Revenue Opportunity', 'Operations', 'Product Catalog', 'Geography'")
    title: str
    severity: str = Field(..., description="'high', 'medium', 'low', 'positive'")
    summary: str
    impact_metric: str
    impact_value: str
    actionable_recommendation: str
    supporting_data: Optional[Dict[str, Any]] = None


class ExecutiveSummary(BaseModel):
    headline: str
    health_score: int
    primary_revenue_driver: str
    top_operational_leak: str
    recommended_focus_area: str


class InsightsResponse(BaseModel):
    executive_summary: ExecutiveSummary
    insights: List[InsightItem]
    generated_at: str
    engine_version: str
