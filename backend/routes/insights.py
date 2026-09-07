"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
API ROUTES: AI BUSINESS INSIGHTS
================================================================================
"""

from fastapi import APIRouter, HTTPException
from backend.services.insights_service import InsightsService
from backend.schemas.insights import InsightsResponse

router = APIRouter(prefix="/api/insights", tags=["AI Business Insights"])


@router.get("", response_model=InsightsResponse, summary="Get AI-Driven Business Insights & Recommendations")
def get_ai_insights():
    try:
        return InsightsService.generate_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")
