"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
API ROUTES: MACHINE LEARNING PREDICTION
================================================================================
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from backend.services.ml_service import MlPredictionService
from backend.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter(prefix="/api/predictions", tags=["ML Predictions"])


@router.post("", response_model=PredictionResponse, summary="Generate Multi-Day Category Demand & Revenue Forecast (POST)")
def generate_forecast_post(request: PredictionRequest):
    try:
        return MlPredictionService.predict_demand(request)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


@router.get("", response_model=PredictionResponse, summary="Generate Multi-Day Category Demand & Revenue Forecast (GET)")
def generate_forecast_get(
    category: str = Query("Set", description="Category name (e.g. Set, Kurta, Western Dress, Top, Saree)"),
    forecast_days: int = Query(14, ge=1, le=60, description="Forecast horizon in days"),
    promotion_ratio: Optional[float] = Query(None, ge=0.0, le=1.0, description="Optional custom promotion ratio"),
    b2b_ratio: Optional[float] = Query(None, ge=0.0, le=1.0, description="Optional custom B2B ratio"),
):
    try:
        req = PredictionRequest(
            category=category,
            forecast_days=forecast_days,
            promotion_ratio=promotion_ratio,
            b2b_ratio=b2b_ratio,
        )
        return MlPredictionService.predict_demand(req)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


@router.get("/actual-vs-predicted", summary="Get 14-Day Holdout Test Set Actual vs Predicted Sales")
def get_actual_vs_predicted(category: Optional[str] = Query(None, description="Optional category filter")):
    import os
    import pandas as pd
    
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "ML", "outputs", "predictions_test_set.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Holdout test predictions file not found")
        
    df = pd.read_csv(csv_path)
    if category and category != "ALL":
        df = df[df["Category"].str.lower() == category.lower()]
        
    return {
        "total_records": len(df),
        "data": df.to_dict(orient="records"),
    }


@router.get("/benchmarks", summary="Get ML Benchmark Model Comparisons & Evaluation Metrics")
def get_benchmarks():
    import os
    import json
    import pandas as pd
    
    base_ml = os.path.join(os.path.dirname(__file__), "..", "..", "ML", "outputs")
    comp_csv = os.path.join(base_ml, "model_comparison.csv")
    metrics_json = os.path.join(base_ml, "evaluation_metrics.json")
    
    models = []
    if os.path.exists(comp_csv):
        models = pd.read_csv(comp_csv).to_dict(orient="records")
        
    metrics = {}
    if os.path.exists(metrics_json):
        with open(metrics_json, "r") as f:
            metrics = json.load(f)
            
    return {
        "models": models,
        "best_model_metrics": metrics,
    }
