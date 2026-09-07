# AI-Powered E-Commerce Analytics — FastAPI Backend API

High-performance, production-ready REST API built with **FastAPI**, **PostgreSQL** (with in-memory SQL mirror fallback), and **Scikit-Learn Machine Learning Pipeline**.

---

## 🚀 Key Features

* **Real Analytics Engine**: Computes high-precision multi-dimensional aggregations over **128,975 sales records** without fabricated numbers.
* **Integrated ML Forecaster**: Invokes serialized Gradient Boosting Regressor (`best_sales_demand_model.joblib`) for multi-day apparel demand and revenue forecasting.
* **AI Business Insights**: Rule-based intelligence engine generating actionable commercial observations and operational leak analysis.
* **Dynamic Filter Architecture**: All analytics endpoints support multi-criteria filtering across Date Ranges, Apparel Categories, Shipping States, Order Statuses, Fulfilment Types, and Sales Channels.
* **Interactive OpenAPI / Swagger Documentation**: Available at `/docs` and `/redoc`.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI (Python 3.10+)
* **ASGI Server**: Uvicorn
* **Data & SQL Engine**: SQLAlchemy, Psycopg2, Pandas, SQLite in-memory engine
* **Machine Learning**: Scikit-Learn, Joblib, NumPy
* **Data Validation**: Pydantic v2

---

## 📁 Directory Structure

```text
backend/
├── main.py                     # FastAPI application entrypoint & middleware
├── requirements.txt            # Python dependencies
├── test_api.py                 # Automated API test suite (13 validation checks)
├── .env.example                # Sample environment configuration
├── database/
│   ├── __init__.py
│   └── connection.py           # DB connection manager & SQL query engine
├── schemas/
│   ├── __init__.py
│   ├── analytics.py            # Pydantic models for KPIs, charts, filters
│   ├── prediction.py           # Pydantic models for ML forecast requests/responses
│   └── insights.py             # Pydantic models for AI Business Insights
├── services/
│   ├── __init__.py
│   ├── analytics_service.py    # Analytical queries & metric calculations
│   ├── ml_service.py           # Machine learning inference & scenario simulation
│   └── insights_service.py     # AI strategic insights & Pareto analysis
└── routes/
    ├── __init__.py
    ├── analytics.py            # REST endpoints for KPIs, trends, geography, products
    ├── predictions.py          # REST endpoints for ML demand forecasting
    └── insights.py             # REST endpoints for AI business recommendations
```

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description | Query / Body Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | API & DB health check | None |
| `GET` | `/api/filter-options` | Available dropdown filter values | None |
| `GET` | `/api/kpis` | Executive KPI scorecard | `start_date`, `end_date`, `category`, `state`, `status`, `fulfilment`, `sales_channel` |
| `GET` | `/api/sales-trend` | Monthly & Daily revenue trend | `granularity` (`monthly` \| `daily`), filters |
| `GET` | `/api/categories` | Category revenue, share & realization | Filters |
| `GET` | `/api/top-products` | Top 10 garment styles and SKUs | `limit` (default: 10), filters |
| `GET` | `/api/geography` | Regional & city-level sales | `state_limit`, `city_limit`, filters |
| `GET` | `/api/order-status` | Order status distribution | Filters |
| `GET` | `/api/fulfilment` | Amazon FBA vs Merchant metrics | Filters |
| `GET` | `/api/sales-channel` | Sales channel performance | Filters |
| `POST` | `/api/predictions` | 1-60 day ML demand & revenue forecast | `{ category, forecast_days, promotion_ratio, b2b_ratio }` |
| `GET` | `/api/predictions` | GET version for quick forecast queries | `category`, `forecast_days` |
| `GET` | `/api/insights` | Curated AI business intelligence | None |

---

## 🏃‍♂️ How to Run the Backend

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp backend/.env.example backend/.env
```

### 3. Run FastAPI Dev Server
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at:
* **Base URL**: `http://localhost:8000`
* **Interactive Docs (Swagger UI)**: `http://localhost:8000/docs`
* **Alternative Docs (ReDoc)**: `http://localhost:8000/redoc`

### 4. Run Automated Test Suite
```bash
python -m backend.test_api
```
