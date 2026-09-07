# AI-Powered E-Commerce Analytics Dashboard

An end-to-end, production-grade data analytics, machine learning, and full-stack web application providing executive business intelligence, multi-dimensional sales analytics, operational visibility, and predictive demand forecasting over **128,975 Amazon e-commerce transactions**.

---

## 🏗️ End-to-End System Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│              React + TypeScript Modern Dashboard              │
│    (Vite, CSS Design System, Recharts, Lucide Icons)          │
└───────────────────────────────┬───────────────────────────────┘
                                │ HTTP REST APIs (JSON)
┌───────────────────────────────▼───────────────────────────────┐
│                    FastAPI Backend Server                     │
│         (Uvicorn, Pydantic v2, CORS, Request Middleware)      │
├───────────────────────────────┬───────────────────────────────┤
│    Analytics & SQL Engine     │   ML & AI Intelligence Engine │
│ (PostgreSQL / SQLite Mirror)  │  (Gradient Boosting Regressor)│
└───────────────┬───────────────┴───────────────┬───────────────┘
                │                               │
┌───────────────▼───────────────┐ ┌─────────────▼───────────────┐
│      PostgreSQL Database      │ │   Serialized ML Artifacts   │
│     `amazon_sales` Table      │ │ `best_sales_demand_model`   │
│     (128,975 sales records)   │ │  `feature_metadata.json`    │
└───────────────────────────────┘ └─────────────────────────────┘
```

---

## 🌟 Project Phases & Capabilities

1. **Phase 1: Data Understanding & Profiling**: Comprehensive data audit identifying schema constraints, 69 state name variations, and invalid postal codes across 128,975 records.
2. **Phase 2: Data Cleaning & Feature Engineering**: Standardized date parsing, zero-padded PIN validation, handled cancellations, and enforced financial invariant ($\text{Realized\_Revenue} \le \text{Gross\_Amount}$).
3. **Phase 3: Exploratory Data Analysis (EDA)**: Generated 20 visual plots, 7 structured aggregations, and identified core revenue pillars (*Set* & *Kurta* generating 82% of revenue).
4. **Phase 4: PostgreSQL Database & SQL Analytics**: Created optimized schema with indexing and developed 12 SQL analysis modules (CTEs, Window Functions, MoM growth, Pareto 80/20).
5. **Phase 5: Power BI Business Intelligence Dashboard**: Star Schema dimensional model with dedicated DAX measures across Executive Overview, Product & Regional Analysis, and Operational Efficiency pages.
6. **Phase 6: Machine Learning Demand & Sales Forecaster**: Trained and evaluated 4 algorithms (Linear Regression, Random Forest, Gradient Boosting, Ridge). Serialized best-performing Gradient Boosting Regressor (Test $R^2 = 0.946$) with recursive multi-step forecasting engine.
7. **Phase 7: FastAPI REST API & Interactive React Web Dashboard**: Full-stack application layer connecting database, ML inference, and analytical rule engines to a sleek, responsive React TypeScript user interface.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend UI** | React 19, TypeScript, Vite, Recharts, Lucide React, Glassmorphic CSS Design System |
| **Backend API** | FastAPI, Uvicorn, Pydantic v2, Python 3.10+ |
| **Database & SQL Engine** | PostgreSQL 14+, SQLAlchemy, Psycopg2, In-Memory SQL Engine |
| **Machine Learning & AI** | Scikit-Learn (Gradient Boosting Regressor), Joblib, NumPy, Pandas |
| **BI & Analytics** | Power BI, DAX Measures, Star Schema Data Modeling |

---

## 📊 Executive Business KPIs (Verified)

| Metric | Value | Business Definition |
| :--- | :--- | :--- |
| **Total Realized Net Revenue** | **₹70,285,702.00** | Net recognized revenue after cancellations/returns (89.43% conversion). |
| **Total Gross Listed Amount** | **₹78,592,678.30** | Gross catalogue demand value. |
| **Total Unique Customer Orders** | **120,378** | Unique customer shopping transactions. |
| **Total Units Dispatched** | **116,649 units** | Cumulative garment units fulfilled. |
| **Average Order Value (AOV)** | **₹583.87** | Realized net income per customer order. |
| **Overall Cancellation Rate** | **14.21%** | 18,332 orders cancelled before delivery (₹6.92M unrealized). |
| **Overall Return Rate** | **1.64%** | 2,109 transactions returned post-dispatch. |
| **Promotion Usage Rate** | **61.89%** | Orders leveraging discount codes and coupon campaigns. |

---

## 📁 Repository Structure

```text
AI-Ecommerce-Analytics-Dashboard/
├── backend/                            # Phase 7: FastAPI REST API
│   ├── main.py                         # Application entrypoint & middleware
│   ├── requirements.txt                # Python backend dependencies
│   ├── test_api.py                     # 13-point automated test suite
│   ├── database/connection.py          # PostgreSQL & SQL database engine
│   ├── schemas/                        # Pydantic schemas (KPIs, ML, Insights)
│   ├── services/                       # Business logic (Analytics, ML, Insights)
│   ├── routes/                         # REST endpoints (analytics, predictions, insights)
│   └── README.md                       # Backend technical documentation
├── frontend/                           # Phase 7: React + TypeScript Web Dashboard
│   ├── index.html                      # HTML entrypoint
│   ├── package.json                    # Frontend dependencies
│   ├── vite.config.ts                  # Vite config with backend proxy
│   ├── src/
│   │   ├── App.tsx                     # Master layout and tab navigation
│   │   ├── index.css                   # Glassmorphic CSS design system
│   │   ├── types/index.ts              # TypeScript API definitions
│   │   ├── services/api.ts             # API client service
│   │   └── components/                 # Reusable UI component library
│   └── README.md                       # Frontend documentation
├── ML/                                 # Phase 6: Machine Learning Pipeline
│   ├── model_training.py               # 4-model training & evaluation script
│   ├── predict.py                      # Standalone CLI & module inference engine
│   ├── models/
│   │   ├── best_sales_demand_model.joblib # Serialized Gradient Boosting Model
│   │   └── feature_metadata.json       # Feature metadata & configuration
│   └── outputs/                        # Residual plots, feature importance, benchmarks
├── Sql/                                # Phase 4: PostgreSQL & SQL Analytics
│   ├── schema.sql                      # PostgreSQL DDL table & index definitions
│   ├── sales_analysis.sql              # 12 business SQL analysis query modules
│   ├── load_to_postgres.py             # Automated PostgreSQL ingestion script
│   └── validate_sql_queries.py         # SQL assertion validation runner
├── PowerBI/                            # Phase 5: Power BI Decision Support System
│   ├── dax_measures.dax                # Production DAX measures library
│   ├── powerbi_dashboard_guide.md      # UI/UX visual formatting blueprint
│   ├── generate_star_schema_tables.py  # Fact and Dimension table generator
│   └── Model_Tables/                   # Star Schema CSV tables
├── Analysis/                           # Phases 1-3: Data Cleaning & Exploratory Analysis
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.py
│   ├── 03_eda.py
│   └── data_cleaning_report.md
├── Data/
│   ├── Raw Data/amazon_sales.csv.csv   # Original raw dataset
│   └── Processed/amazon_sales_analytics.csv # Analytics dataset (128,975 rows)
├── .env.example                        # Root environment template
└── README.md                           # Master project documentation
```

---

## 🚀 How to Run the Application

### Option A: Running Backend & Frontend Together

#### Step 1: Start Backend API
```bash
# In project root:
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
* Backend API: `http://localhost:8000`
* Interactive API Documentation: `http://localhost:8000/docs`

#### Step 2: Start React Frontend
```bash
# In a new terminal:
cd frontend
npm install
npm run dev
```
* Web Dashboard: `http://localhost:5173`

---

## 🧪 Automated Testing & Verification

Run the comprehensive backend validation suite:
```bash
python -m backend.test_api
```
Tests all 13 core REST endpoints, dynamic multi-criteria filters, PostgreSQL/SQL engine queries, Scikit-Learn ML predictions, and AI Business Insights generation.

---

## 📈 Machine Learning Benchmark & Results

We benchmarked 4 regression models on a chronological time-based 80/20 train/test split:

| Model Algorithm | Test $R^2$ Score | Test MAE (INR) | Test RMSE (INR) | Decision / Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting Regressor** | **0.946** (94.6%) | **₹14,205.50** | **₹28,497.10** | **Selected Best Model (Serialized)** |
| Random Forest Regressor | 0.938 (93.8%) | ₹15,840.20 | ₹30,812.40 | Robust non-linear benchmark |
| Ridge Regressor ($\alpha=1.0$) | 0.884 (88.4%) | ₹23,120.40 | ₹42,150.90 | Regularized linear baseline |
| Linear Regression (OLS) | 0.882 (88.2%) | ₹23,450.80 | ₹42,680.10 | Baseline model |

### Top Predictive Features
1. `rolling_mean_7`: 7-day category moving average revenue
2. `lag_1`: Previous day realized category revenue
3. `cat_Set` & `cat_Kurta`: Apparel category indicator dummies
4. `Day_of_Week` & `Is_Weekend`: Weekly cyclical demand patterns
5. `Promotion_Ratio`: Active discount campaign frequency

---

## 💡 Key Business Insights Discovered

1. **Category Concentration**: **82.16% of gross revenue** is anchored in just two apparel categories: *Set* (₹35.03M, 49.84%) and *Kurta* (₹19.08M, 27.15%).
2. **Pre-Delivery Cancellation Leakage**: Total lost/unrealized revenue stands at **₹8.31M** (10.57% of demand), primarily driven by an overall **14.21% cancellation rate** (₹6.92M) occurring before dispatch.
3. **Regional Market Concentration**: The top 3 states (**Maharashtra**, **Karnataka**, and **Telangana**) generate **39.50% of total nationwide revenue** (₹27.76M), indicating strong urban Tier-1 market adoption.
4. **FBA Fulfillment Superiority**: Amazon FBA achieves a **93.14% financial realization rate** with lower return rates (1.48%) compared to merchant-fulfilled dispatches (81.14% realization, 17.47% cancellation).
5. **B2B Growth Potential**: B2B wholesale buyers exhibit an Average Order Value **2.4x higher than standard retail shoppers**, representing a high-margin expansion vector.

---

## 📸 Screenshots & Visual Assets

Visual artifacts are cataloged in [`docs/screenshots/`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/docs/screenshots/):
* `actual_vs_predicted.png`: Regression fit test scatter plot ($R^2 = 0.946$).
* `feature_importance.png`: Feature weight distribution for demand forecasting.
* `daily_sales_forecast_plot.png`: 14-day forward sales trajectory projection.
* `monthly_revenue_trend.png`: Gross vs Realized revenue historical trend.
* `category_revenue.png`: Category revenue share rankings.
* `top_states_revenue.png`: Geographic state market concentration.

---

## 🔮 Realistic Future Improvements

1. **Real-Time Streaming Ingestion**: Integrate Apache Kafka / AWS Kinesis to ingest and process live order webhooks with sub-second dashboard updates.
2. **Distributed Caching**: Add Redis caching for high-frequency analytical API queries (`/api/kpis`, `/api/geography`).
3. **Automated ML Retraining**: Deploy MLflow tracking and automated monthly retraining pipelines as new seasonal transaction batches are ingested.
4. **LLM-Powered Natural Language Analytics**: Integrate Gemini / OpenAI function-calling APIs to allow executives to query data in conversational English (e.g., *"What caused the revenue dip in week 22?"*).
5. **Automated Stockout Alerts**: Push Slack / WhatsApp webhook notifications when predicted 7-day demand exceeds current warehouse inventory levels.

---

## 🎯 Interview & Technical Presentation

For technical interview preparation, system design questions, architecture trade-offs, and 20 detailed Q&As, review the complete [Technical Interview Guide](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/docs/INTERVIEW_GUIDE.md).

