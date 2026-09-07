"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
PHASE 6: STANDALONE PREDICTION & INFERENCE ENGINE (ML/predict.py)
================================================================================
Purpose:
  Provides a production-ready, standalone inference pipeline that loads the
  serialized Machine Learning model (best_sales_demand_model.joblib) and
  generates multi-day sales and demand forecasts for any apparel category.

Architecture / Integration:
  - Can be executed directly via Command Line Interface (CLI).
  - Can be imported as a Python module by FastAPI / Flask backend routes.
  - Returns structured JSON payloads for frontend dashboard charts and widgets.
================================================================================
"""

import os
import sys
import json
import argparse
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ==============================================================================
# CONFIGURATION & PATH SETUP
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ML', 'models', 'best_sales_demand_model.joblib')
METADATA_PATH = os.path.join(BASE_DIR, 'ML', 'models', 'feature_metadata.json')
DATA_PATH = os.path.join(BASE_DIR, 'Data', 'Processed', 'amazon_sales_analytics.csv')


# ==============================================================================
# 1. MODEL & METADATA LOADER
# ==============================================================================
def load_model_and_metadata():
    """
    Loads the serialized model artifact and feature metadata dictionary.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model artifact not found at: {MODEL_PATH}")
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Feature metadata not found at: {METADATA_PATH}")

    model = joblib.load(MODEL_PATH)
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    return model, metadata


# ==============================================================================
# 2. FEATURE EXTRACTION FOR INFERENCE
# ==============================================================================
def extract_latest_category_features(category_name, data_path=DATA_PATH):
    """
    Extracts the latest historical state (lags, rolling averages, catalog prices)
    for a given category to initialize forward forecasting.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at: {data_path}")

    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter category
    cat_df = df[df['Category'].str.lower() == category_name.lower()].copy()
    if cat_df.empty:
        available_cats = df['Category'].dropna().unique().tolist()
        raise ValueError(f"Category '{category_name}' not found. Available categories: {available_cats}")

    # Aggregate daily
    daily = cat_df.groupby('Date').agg(
        Realized_Revenue=('Realized_Revenue', 'sum'),
        Gross_Amount=('Gross_Amount', 'sum'),
        Qty=('Qty', 'sum'),
        Line_Count=('Order_ID', 'count'),
        Promo_Count=('Has_Promotion', 'sum'),
        B2B_Count=('Is_B2B', 'sum')
    ).reset_index().sort_values('Date')

    # Fill full date range
    full_idx = pd.date_range(daily['Date'].min(), daily['Date'].max(), freq='D')
    daily = daily.set_index('Date').reindex(full_idx, fill_value=0).reset_index().rename(columns={'index': 'Date'})

    daily['Avg_Gross_Line_Value'] = (daily['Gross_Amount'] / daily['Line_Count'].replace(0, 1)).fillna(0)
    daily['Promotion_Ratio'] = (daily['Promo_Count'] / daily['Line_Count'].replace(0, 1)).fillna(0)
    daily['B2B_Ratio'] = (daily['B2B_Count'] / daily['Line_Count'].replace(0, 1)).fillna(0)

    # Average selling price per unit for demand conversion
    total_revenue = daily['Realized_Revenue'].sum()
    total_units = daily['Qty'].sum()
    avg_unit_price = (total_revenue / total_units) if total_units > 0 else 650.0

    return daily, avg_unit_price


# ==============================================================================
# 3. RECURSIVE MULTI-STEP FORWARD FORECAST GENERATOR
# ==============================================================================
def forecast_sales_demand(category_name: str, forecast_days: int = 14) -> dict:
    """
    Generates a forward forecast of daily realized revenue and unit demand.
    
    Parameters:
      category_name (str): Apparel category name (e.g., 'Set', 'Kurta', 'Western Dress')
      forecast_days (int): Number of days ahead to forecast (default: 14)
      
    Returns:
      dict: Structured forecast payload containing summary KPIs and daily timeline.
    """
    model, metadata = load_model_and_metadata()
    feature_names = metadata['feature_names']
    
    daily_history, avg_unit_price = extract_latest_category_features(category_name)
    last_historical_date = daily_history['Date'].max()

    # Create working buffer of revenue and qty history
    rev_history = list(daily_history['Realized_Revenue'].values)
    qty_history = list(daily_history['Qty'].values)
    
    # Static historical baseline ratios
    avg_promo_ratio = float(daily_history['Promotion_Ratio'].iloc[-14:].mean())
    avg_b2b_ratio = float(daily_history['B2B_Ratio'].iloc[-14:].mean())
    avg_gross_line = float(daily_history['Avg_Gross_Line_Value'].iloc[-14:].mean())

    forecast_records = []
    
    for step in range(1, forecast_days + 1):
        target_date = last_historical_date + timedelta(days=step)
        
        # Build feature vector matching exact training columns
        features = {}
        features['lag_1'] = rev_history[-1]
        features['lag_2'] = rev_history[-2] if len(rev_history) >= 2 else rev_history[-1]
        features['lag_3'] = rev_history[-3] if len(rev_history) >= 3 else rev_history[-1]
        features['lag_7'] = rev_history[-7] if len(rev_history) >= 7 else rev_history[-1]
        features['lag_14'] = rev_history[-14] if len(rev_history) >= 14 else rev_history[-1]

        # Rolling window stats
        recent_7 = rev_history[-7:]
        recent_14 = rev_history[-14:]
        features['rolling_mean_7'] = float(np.mean(recent_7))
        features['rolling_std_7'] = float(np.std(recent_7)) if len(recent_7) > 1 else 0.0
        features['rolling_mean_14'] = float(np.mean(recent_14))

        # Quantity features
        features['qty_lag_1'] = qty_history[-1]
        features['qty_lag_7'] = qty_history[-7] if len(qty_history) >= 7 else qty_history[-1]
        features['qty_rolling_mean_7'] = float(np.mean(qty_history[-7:]))

        # Calendar features
        dow = target_date.dayofweek
        features['Day_of_Week'] = dow
        features['Day_of_Month'] = target_date.day
        features['Month'] = target_date.month
        features['Week_of_Year'] = int(target_date.isocalendar()[1])
        features['Is_Weekend'] = 1 if dow in [5, 6] else 0

        # Commercial ratios
        features['Promotion_Ratio'] = avg_promo_ratio
        features['B2B_Ratio'] = avg_b2b_ratio
        features['Avg_Gross_Line_Value'] = avg_gross_line

        # One-hot category dummies
        for col in feature_names:
            if col.startswith('cat_'):
                cat_suffix = col.replace('cat_', '')
                features[col] = 1 if cat_suffix.lower() == category_name.lower() else 0

        # Construct single-row DataFrame aligned to feature order
        feat_df = pd.DataFrame([features])[feature_names]
        
        # Predict revenue (strictly non-negative)
        pred_rev = float(np.maximum(0, model.predict(feat_df)[0]))
        
        # Estimate corresponding unit demand
        pred_qty = int(round(pred_rev / avg_unit_price)) if avg_unit_price > 0 else 0

        # Append to recursive history buffer for multi-step lags
        rev_history.append(pred_rev)
        qty_history.append(pred_qty)

        forecast_records.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'day_of_week': target_date.strftime('%A'),
            'is_weekend': bool(dow in [5, 6]),
            'predicted_revenue_inr': round(pred_rev, 2),
            'predicted_unit_demand': pred_qty,
            'lower_bound_inr': round(max(0, pred_rev * 0.85), 2),
            'upper_bound_inr': round(pred_rev * 1.15, 2)
        })

    # Summary KPIs
    total_forecast_revenue = sum(r['predicted_revenue_inr'] for r in forecast_records)
    total_forecast_units = sum(r['predicted_unit_demand'] for r in forecast_records)
    daily_avg_revenue = total_forecast_revenue / forecast_days

    result = {
        'status': 'success',
        'category': category_name,
        'forecast_horizon_days': forecast_days,
        'forecast_start_date': forecast_records[0]['date'],
        'forecast_end_date': forecast_records[-1]['date'],
        'kpis': {
            'total_predicted_revenue_inr': round(total_forecast_revenue, 2),
            'total_predicted_unit_demand': total_forecast_units,
            'daily_average_revenue_inr': round(daily_avg_revenue, 2),
            'avg_selling_price_inr': round(avg_unit_price, 2)
        },
        'daily_forecast': forecast_records
    }

    return result


# ==============================================================================
# 4. CLI INTERFACE
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="E-Commerce Category Sales & Demand Forecaster")
    parser.add_argument('--category', type=str, default='Set', help="Apparel category (e.g. Set, Kurta, Western Dress)")
    parser.add_argument('--days', type=int, default=14, help="Forecast horizon in days (default: 14)")
    parser.add_argument('--json', action='store_true', help="Output result formatted as JSON string")

    args = parser.parse_args()

    try:
        forecast_output = forecast_sales_demand(category_name=args.category, forecast_days=args.days)
        
        if args.json:
            print(json.dumps(forecast_output, indent=2))
        else:
            kpis = forecast_output['kpis']
            print("\n" + "=" * 70)
            print(f"  SALES & DEMAND FORECAST REPORT: Category '{forecast_output['category'].upper()}'")
            print("=" * 70)
            print(f"Forecast Horizon : {forecast_output['forecast_start_date']} to {forecast_output['forecast_end_date']} ({forecast_output['forecast_horizon_days']} Days)")
            print(f"Total Predicted Revenue : INR {kpis['total_predicted_revenue_inr']:,.2f}")
            print(f"Total Predicted Demand  : {kpis['total_predicted_unit_demand']:,} Units")
            print(f"Daily Average Revenue   : INR {kpis['daily_average_revenue_inr']:,.2f}")
            print(f"Estimated Avg Unit ASP  : INR {kpis['avg_selling_price_inr']:,.2f}")
            print("-" * 70)
            print(f"{'Date':<12} | {'Day':<10} | {'Predicted Rev (INR)':<20} | {'Demand (Units)':<14}")
            print("-" * 70)
            for row in forecast_output['daily_forecast']:
                print(f"{row['date']:<12} | {row['day_of_week']:<10} | INR {row['predicted_revenue_inr']:>14,.2f} | {row['predicted_unit_demand']:>12,}")
            print("=" * 70 + "\n")
            
    except Exception as e:
        print(f"Error executing prediction: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
