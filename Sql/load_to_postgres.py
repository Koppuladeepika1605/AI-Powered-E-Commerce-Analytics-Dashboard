"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
PHASE 4: POSTGRESQL DATA INGESTION & PIPELINE SCRIPT
================================================================================
Description:
    Automated Python script to ingest the analytics dataset into PostgreSQL.
    Configurable via environment variables (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE).
    Creates database 'ecommerce_analytics' and table 'amazon_sales' with proper types and indexes.

Author: AI Assistant
Date: September 5, 2026
License: MIT
================================================================================
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text

def load_data_to_postgresql():
    print("=" * 80)
    print("     POSTGRESQL DATA INGESTION: E-COMMERCE ANALYTICS PIPELINE")
    print("=" * 80)

    # 1. Environment & Connection Parameters
    pg_host = os.getenv('PGHOST', 'localhost')
    pg_port = os.getenv('PGPORT', '5432')
    pg_user = os.getenv('PGUSER', 'postgres')
    pg_pass = os.getenv('PGPASSWORD', 'postgres')
    pg_db   = os.getenv('PGDATABASE', 'ecommerce_analytics')

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'Data', 'Processed', 'amazon_sales_analytics.csv')
    schema_path = os.path.join(base_dir, 'Sql', 'schema.sql')

    print(f"\n[1/5] Target CSV: {csv_path}")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Error: Processed CSV not found at {csv_path}")

    # 2. Check Database Connection & Create Database if Not Exists
    print(f"\n[2/5] Connecting to PostgreSQL at {pg_host}:{pg_port} as user '{pg_user}'...")
    try:
        # Connect to default 'postgres' database to check/create target database
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_pass,
            dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (pg_db,))
        exists = cursor.fetchone()
        if not exists:
            print(f"  -> Database '{pg_db}' does not exist. Creating database '{pg_db}'...")
            cursor.execute(f"CREATE DATABASE {pg_db};")
            print(f"  -> Database '{pg_db}' created successfully.")
        else:
            print(f"  -> Database '{pg_db}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\n[!] WARNING: Could not connect to PostgreSQL server: {e}")
        print("  -> Please ensure PostgreSQL service is running on your machine.")
        print("  -> You can set credentials via environment variables: PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE.")
        print("  -> You can also run the SQL scripts manually in pgAdmin or psql using 'Sql/schema.sql'.")
        return False

    # 3. Create Table & Indexes using SQLAlchemy
    print(f"\n[3/5] Connecting to target database '{pg_db}'...")
    db_uri = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(db_uri)

    print("  -> Executing DDL from Sql/schema.sql...")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Split by statements and execute
    with engine.begin() as conn:
        for statement in schema_sql.split(';'):
            stmt = statement.strip()
            if stmt and not stmt.startswith('--') and not stmt.startswith('\\'):
                conn.execute(text(stmt))

    print("  -> Table 'amazon_sales' and indexes created successfully.")

    # 4. Load Processed Dataset
    print(f"\n[4/5] Reading processed CSV and ingesting 128,975 rows into 'amazon_sales'...")
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Map column headers to lowercase postgres column names
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

    # Ingest in chunks of 10,000 for high speed and low memory usage
    df.to_sql('amazon_sales', engine, if_exists='append', index=False, chunksize=10000, method='multi')
    print("  -> Data ingestion complete!")

    # 5. Verification Queries
    print("\n[5/5] Running verification checks on PostgreSQL table...")
    with engine.connect() as conn:
        row_count = conn.execute(text("SELECT COUNT(*) FROM amazon_sales;")).scalar()
        gross_sum = conn.execute(text("SELECT SUM(gross_amount) FROM amazon_sales;")).scalar()
        real_sum  = conn.execute(text("SELECT SUM(realized_revenue) FROM amazon_sales;")).scalar()
        order_cnt = conn.execute(text("SELECT COUNT(DISTINCT order_id) FROM amazon_sales;")).scalar()

    print(f"  -> Total Rows in DB:       {row_count:,} (Expected: 128,975)")
    print(f"  -> Total Unique Orders:    {order_cnt:,} (Expected: 120,378)")
    print(f"  -> Total Gross Amount:     INR {float(gross_sum):,_.2f}")
    print(f"  -> Total Realized Revenue: INR {float(real_sum):,_.2f}")

    print("\n" + "=" * 80)
    print("POSTGRESQL INGESTION PIPELINE FINISHED SUCCESSFULLY!")
    print("=" * 80)
    return True

if __name__ == '__main__':
    load_data_to_postgresql()
