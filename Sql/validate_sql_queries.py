"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
PHASE 4: SQL QUERY VALIDATION & ACCURACY VERIFICATION RUNNER
================================================================================
Description:
    Loads 'Data/Processed/amazon_sales_analytics.csv' into an in-memory SQL
    engine and executes the analytical queries from 'Sql/sales_analysis.sql'
    to mathematically verify consistency against Phase 3 Python EDA outputs.

Author: AI Assistant
Date: September 5, 2026
License: MIT
================================================================================
"""

import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

def validate_sql_analysis():
    print("=" * 80)
    print("      PHASE 4: SQL QUERY VALIDATION & CROSS-CHECK RUNNER")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'Data', 'Processed', 'amazon_sales_analytics.csv')
    
    print(f"\n[1/3] Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Standardize column names for SQL compatibility
    df.columns = [
        'order_id', 'order_date', 'order_year', 'order_month', 'month_name',
        'order_week', 'order_day', 'day_name', 'status', 'courier_status',
        'fulfilment', 'fulfilled_by', 'sales_channel', 'ship_service_level',
        'category', 'size', 'style', 'sku', 'asin', 'qty', 'currency',
        'recorded_amount', 'gross_amount', 'realized_revenue', 'ship_city',
        'ship_state', 'ship_postal_code', 'ship_country', 'promotion_ids',
        'has_promotion', 'is_b2b', 'is_cancelled', 'is_delivered', 'is_returned',
        'is_realized', 'is_valid_pin'
    ]

    # Create in-memory SQLite engine
    engine = create_engine('sqlite:///:memory:')
    df.to_sql('amazon_sales', engine, index=False)
    print(f"  -> Ingested {len(df):,} rows into SQL engine.")

    # 2. Run Key Analytical Queries
    print("\n[2/3] Executing Core SQL Business Queries...")
    
    with engine.connect() as conn:
        # Query 1: Executive KPIs
        q1 = """
        SELECT 
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(*) AS total_lines,
            SUM(qty) AS total_units,
            ROUND(SUM(gross_amount), 2) AS gross_amount,
            ROUND(SUM(realized_revenue), 2) AS realized_revenue,
            ROUND(SUM(gross_amount) - SUM(realized_revenue), 2) AS lost_value,
            ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
            ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
            ROUND(SUM(CASE WHEN is_returned THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS return_rate_pct
        FROM amazon_sales;
        """
        res1 = pd.read_sql(q1, conn)
        print("\n--- SQL Query 1: Executive KPI Scorecard ---")
        print(res1.to_string(index=False))

        # Query 2: Monthly Trends
        q2 = """
        SELECT 
            order_year,
            order_month,
            month_name,
            COUNT(DISTINCT order_id) AS orders,
            ROUND(SUM(realized_revenue), 2) AS realized_revenue,
            ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
        FROM amazon_sales
        GROUP BY order_year, order_month, month_name
        ORDER BY order_year, order_month;
        """
        res2 = pd.read_sql(q2, conn)
        print("\n--- SQL Query 2: Monthly Sales & Realization Trends ---")
        print(res2.to_string(index=False))

        # Query 3: Category Performance
        q3 = """
        SELECT 
            category,
            COUNT(*) AS transactions,
            ROUND(SUM(realized_revenue), 2) AS realized_revenue,
            ROUND(SUM(realized_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS rev_share_pct,
            ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
        FROM amazon_sales
        GROUP BY category
        ORDER BY realized_revenue DESC;
        """
        res3 = pd.read_sql(q3, conn)
        print("\n--- SQL Query 3: Category Performance & Share ---")
        print(res3.to_string(index=False))

        # Query 4: Top 5 States
        q4 = """
        SELECT 
            ship_state,
            COUNT(DISTINCT order_id) AS orders,
            ROUND(SUM(realized_revenue), 2) AS realized_revenue,
            ROUND(SUM(realized_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS rev_share_pct
        FROM amazon_sales
        GROUP BY ship_state
        ORDER BY realized_revenue DESC
        LIMIT 5;
        """
        res4 = pd.read_sql(q4, conn)
        print("\n--- SQL Query 4: Top 5 Revenue-Generating States ---")
        print(res4.to_string(index=False))

        # Query 5: Fulfillment Comparison
        q5 = """
        SELECT 
            fulfilment,
            COUNT(*) AS order_lines,
            ROUND(SUM(realized_revenue), 2) AS realized_revenue,
            ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
            ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
        FROM amazon_sales
        GROUP BY fulfilment
        ORDER BY realized_revenue DESC;
        """
        res5 = pd.read_sql(q5, conn)
        print("\n--- SQL Query 5: Amazon FBA vs Merchant Fulfillment ---")
        print(res5.to_string(index=False))

    # 3. Validation Cross-Check Assertions
    print("\n[3/3] Cross-Checking SQL Aggregations vs Phase 3 Python Results...")
    assert int(res1['total_orders'].iloc[0]) == 120378, "Order count mismatch!"
    assert int(res1['total_lines'].iloc[0]) == 128975, "Line count mismatch!"
    assert float(res1['gross_amount'].iloc[0]) == 78592678.30, "Gross amount mismatch!"
    assert float(res1['realized_revenue'].iloc[0]) == 70285702.00, "Realized revenue mismatch!"
    assert float(res1['lost_value'].iloc[0]) == 8306976.30, "Lost value mismatch!"
    assert float(res1['realization_rate_pct'].iloc[0]) == 89.43, "Realization rate mismatch!"
    assert float(res1['cancellation_rate_pct'].iloc[0]) == 14.21, "Cancellation rate mismatch!"
    assert float(res1['return_rate_pct'].iloc[0]) == 1.64, "Return rate mismatch!"

    print("  -> ALL SQL VALIDATION ASSERTIONS PASSED WITH 100% PRECISION!")
    print("\n" + "=" * 80)
    print("PHASE 4 SQL ANALYSIS & VALIDATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == '__main__':
    validate_sql_analysis()
