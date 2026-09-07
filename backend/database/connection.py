"""
================================================================================
AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
DATABASE CONNECTION & QUERY ENGINE LAYER
================================================================================
Description:
    Manages connections to PostgreSQL database with seamless fallback to the
    processed analytics dataset (128,975 rows) to ensure 100% data reliability,
    zero mock data, and instant responsiveness.
================================================================================
"""

import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Optional, Tuple, Any

# Resolve paths
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BACKEND_DIR)
DEFAULT_CSV_PATH = os.path.join(ROOT_DIR, "Data", "Processed", "amazon_sales_analytics.csv")


class DatabaseManager:
    _instance = None
    _engine: Optional[Engine] = None
    _is_postgres: bool = False
    _sqlite_conn: Optional[sqlite3.Connection] = None
    _df_cache: Optional[pd.DataFrame] = None

    def __init__(self):
        self.csv_path = os.getenv("DATA_CSV_PATH", DEFAULT_CSV_PATH)
        if not os.path.isabs(self.csv_path):
            self.csv_path = os.path.join(ROOT_DIR, self.csv_path)

        self.pg_host = os.getenv("PGHOST", "localhost")
        self.pg_port = os.getenv("PGPORT", "5432")
        self.pg_user = os.getenv("PGUSER", "postgres")
        self.pg_pass = os.getenv("PGPASSWORD", "postgres")
        self.pg_db = os.getenv("PGDATABASE", "ecommerce_analytics")
        self.db_url = os.getenv(
            "DATABASE_URL",
            f"postgresql+psycopg2://{self.pg_user}:{self.pg_pass}@{self.pg_host}:{self.pg_port}/{self.pg_db}",
        )
        self.initialize_engine()

    @classmethod
    def get_instance(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize_engine(self):
        """Attempts connection to PostgreSQL, falls back to SQLite in-memory mirror of dataset."""
        try:
            pg_engine = create_engine(self.db_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
            with pg_engine.connect() as conn:
                res = conn.execute(text("SELECT COUNT(*) FROM amazon_sales;")).scalar()
                if res and res > 0:
                    self._engine = pg_engine
                    self._is_postgres = True
                    print(f"[*] DatabaseManager: Connected to PostgreSQL ('{self.pg_db}', {res:,} records).")
                    return
        except Exception as e:
            print(f"[!] DatabaseManager: PostgreSQL not connected ({e}). Initializing high-speed SQL analytics engine...")

        # Fallback to in-memory SQLite mirror of the exact processed 128,975 dataset
        self._is_postgres = False
        self._init_sqlite_engine()

    def _init_sqlite_engine(self):
        """Loads processed dataset into an in-memory SQLite database for blazing-fast parameterized queries."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Processed analytics dataset missing at: {self.csv_path}")

        print(f"[*] DatabaseManager: Ingesting dataset from {self.csv_path} into SQL Engine...")
        df = pd.read_csv(self.csv_path, low_memory=False)
        
        # Standardize column names matching Sql/schema.sql
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
        
        # Cast dates and booleans for clean SQL operations
        df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')
        
        # Create SQLite memory connection
        self._sqlite_conn = sqlite3.connect(":memory:", check_same_thread=False)
        df.to_sql("amazon_sales", self._sqlite_conn, if_exists="replace", index=False)
        
        # Create indexes for sub-millisecond query filtering
        cursor = self._sqlite_conn.cursor()
        cursor.execute("CREATE INDEX idx_sq_date ON amazon_sales(order_date);")
        cursor.execute("CREATE INDEX idx_sq_cat ON amazon_sales(category);")
        cursor.execute("CREATE INDEX idx_sq_state ON amazon_sales(ship_state);")
        cursor.execute("CREATE INDEX idx_sq_status ON amazon_sales(status);")
        cursor.execute("CREATE INDEX idx_sq_fulfil ON amazon_sales(fulfilment);")
        cursor.execute("CREATE INDEX idx_sq_channel ON amazon_sales(sales_channel);")
        self._sqlite_conn.commit()
        
        self._df_cache = df
        print(f"[*] DatabaseManager: SQL Engine ready ({len(df):,} records indexed).")

    @property
    def is_postgres(self) -> bool:
        return self._is_postgres

    def execute_query_df(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """Executes a SQL query and returns a pandas DataFrame."""
        if self._is_postgres and self._engine:
            try:
                with self._engine.connect() as conn:
                    return pd.read_sql_query(text(query), conn, params=params or {})
            except Exception as e:
                print(f"[!] PostgreSQL query execution failed: {e}. Falling back to SQL cache engine.")
                if self._sqlite_conn is None:
                    self._init_sqlite_engine()

        # SQLite query execution
        conn = self._sqlite_conn
        if conn is None:
            self._init_sqlite_engine()
            conn = self._sqlite_conn

        # Format boolean comparisons for SQLite compatibility if needed
        sqlite_query = query
        # SQLite uses 1/0 for boolean columns
        # In our SQL query strings, boolean constants TRUE/FALSE are supported by SQLite 3.23+
        return pd.read_sql_query(sqlite_query, conn, params=params or {})

    def get_raw_dataframe(self) -> pd.DataFrame:
        """Returns the cached raw DataFrame for fast in-memory operations and ML feature extraction."""
        if self._df_cache is None:
            df = pd.read_csv(self.csv_path, low_memory=False)
            self._df_cache = df
        return self._df_cache


db_manager = DatabaseManager.get_instance()
