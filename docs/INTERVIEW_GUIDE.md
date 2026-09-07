# AI-Powered E-Commerce Analytics Dashboard — Technical Interview Guide

A comprehensive, production-backed preparation guide for technical interviews, system design discussions, and portfolio walkthroughs.

---

## ⚡ 1. Project Elevator Pitches

### 30-Second Elevator Pitch
> *"I built an end-to-end AI-Powered E-Commerce Analytics Dashboard that analyzes 128,975 Amazon retail transactions and forecasts multi-day apparel demand. The system features an automated Python cleaning pipeline, a PostgreSQL analytical database, a Power BI Star-Schema reporting suite, a trained Gradient Boosting demand forecasting model ($R^2 = 0.946$), a FastAPI REST backend, and an interactive React TypeScript dashboard with glassmorphic UI."*

### 1-Minute Elevator Pitch
> *"The AI-Powered E-Commerce Analytics Dashboard is a full-stack data analytics and machine learning solution designed to solve operational blind spots in high-volume retail. Starting with 128,975 raw transactional records totaling ₹78.59M in gross sales, I developed a Python pipeline that standardized 69 messy state variants, enforced financial invariants, and generated a 36-column analytics dataset. I loaded this into PostgreSQL with indexes and analyzed it through 12 SQL modules including Pareto 80/20 and MoM window functions.*
> 
> *To solve inventory stockouts, I engineered 28 lag, rolling, and promotional features and trained a Gradient Boosting Regressor achieving an $R^2$ of 0.946. Finally, I built a modular FastAPI REST API and a responsive React TypeScript frontend featuring dynamic multi-criteria filtering, live demand forecasting with confidence intervals, and automated AI business insights."*

---

## 🏗️ 2. Architecture & Technology Justification

```text
┌────────────────────────────────────────────────────────┐
│             React + TypeScript Frontend                │
│       (Vite, Recharts, Lucide Icons, Glassmorphism)    │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP / JSON REST APIs
┌──────────────────────────▼─────────────────────────────┐
│                 FastAPI Backend Server                 │
│              (Uvicorn, Pydantic, CORS)                 │
├──────────────────────────┬─────────────────────────────┤
│   Analytics & SQL Engine │   ML & Inference Engine     │
│   (PostgreSQL / SQL Engine) (GradientBoostingRegressor)│
└──────────────┬───────────┴───────────────┬─────────────┘
               │                           │
┌──────────────▼───────────┐ ┌─────────────▼─────────────┐
│    PostgreSQL Database   │ │ Serialized ML Artifacts   │
│   `amazon_sales` Table   │ │ `best_sales_demand_model` │
│     (128,975 records)    │ │ `feature_metadata.json`   │
└──────────────────────────┘ └───────────────────────────┘
```

### Technology Justifications:
* **Python (Pandas/NumPy)**: Industry-standard for complex data wrangling, vectorized feature engineering, and statistical analysis.
* **PostgreSQL & SQL**: Robust ACID-compliant relational storage with B-tree indexing for sub-second analytical aggregations across 128k+ rows.
* **Scikit-Learn (Gradient Boosting Regressor)**: Superior non-linear regression capability handling categorical one-hot features, non-stationary daily seasonality, and multi-day lags.
* **FastAPI**: Modern, async-first Python web framework offering automatic OpenAPI documentation, strict Pydantic v2 data validation, and native JSON serialization.
* **React + TypeScript + Vite**: Ultra-fast hot module replacement, strict compile-time type safety for complex analytical models, and rich declarative UI rendering with Recharts.

---

## 🔍 3. Deep-Dive Explanations by Component

### Data Cleaning & Integrity (Phase 2)
* **Messy State Names**: Standardized 69 variations (e.g., `'NL'`, `'PB'`, `'bihar'`, `'delhi'`) into 38 canonical Indian States and Union Territories.
* **Date Parsing**: Converted arbitrary date strings to `datetime64[ns]` and extracted Year, Month, Month Name, Week of Year, and Day Name.
* **PIN Code Validation**: Cleaned 6-digit postal codes, handled leading zeros, and flagged malformed codes.
* **Financial Invariant**: Enforced $\text{Realized\_Revenue} = 0.0$ for cancelled and returned items, ensuring $\text{Realized\_Revenue} \le \text{Gross\_Amount}$ with 0 violations across 128,975 rows.

### Exploratory Data Analysis (Phase 3)
* **Volume vs Revenue**: April was the peak trading month (₹25.67M realized), with a gradual decline in May (₹23.47M) and June (₹21.05M).
* **Category Dominance**: The catalog is heavily Pareto-concentrated: *Set* (49.84% share, ₹35.03M) and *Kurta* (27.15% share, ₹19.08M) drive **82% of gross revenue**.
* **Geographic Powerhouses**: Maharashtra (₹12.05M, 17.15%), Karnataka (₹9.52M, 13.55%), and Telangana (₹6.18M, 8.80%) represent the top 3 markets.

### SQL Analytics & Window Functions (Phase 4)
* **Month-over-Month (MoM) Growth**: Used `LAG() OVER (ORDER BY order_year, order_month)` to track order contraction (-14.47% in May, -10.40% in June).
* **Pareto 80/20 Garment Styles**: Used CTEs and cumulative window sums `SUM(style_revenue) OVER (ORDER BY style_revenue DESC) / SUM(style_revenue) OVER ()` to isolate the top 80% revenue-driving styles.
* **Average Order Value (AOV)**: Evaluated basket size metrics, finding completed orders have an average realized AOV of ₹583.87.

### Power BI & DAX Modeling (Phase 5)
* **Star Schema**: Modeled data into 1 central Fact table (`Fact_AmazonSales`) connected in 1-to-many single-direction relationships to 5 Dimension tables (`Dim_Date`, `Dim_Product`, `Dim_Geography`, `Dim_OrderStatus`, `Dim_Fulfilment`).
* **DAX Measures**: Created dedicated `_Measures` table housing clean calculations using `CALCULATE`, `DIVIDE`, `SUMX`, and time-intelligence expressions.

### Machine Learning Demand Forecasting (Phase 6)
* **Problem Formulation**: Formulated as a daily category-level multi-step revenue and unit demand regression task.
* **Feature Engineering**: Built 28 features including 5 revenue lag windows (`lag_1`, `lag_2`, `lag_3`, `lag_7`, `lag_14`), rolling window aggregations (`rolling_mean_7`, `rolling_std_7`, `rolling_mean_14`), quantity lags (`qty_lag_1`, `qty_lag_7`), calendar attributes (`Day_of_Week`, `Month`, `Is_Weekend`), commercial ratios (`Promotion_Ratio`, `B2B_Ratio`, `Avg_Gross_Line_Value`), and one-hot category encodings.
* **Model Benchmarking**: Evaluated 4 models on time-based test split:
  1. **Gradient Boosting Regressor**: **$R^2 = 0.946$**, $\text{MAE} = ₹14,205.50$, $\text{RMSE} = ₹28,497.10$ *(Selected Best)*
  2. Random Forest Regressor: $R^2 = 0.938$, $\text{MAE} = ₹15,840.20$
  3. Ridge Regressor: $R^2 = 0.884$, $\text{MAE} = ₹23,120.40$
  4. Linear Regression: $R^2 = 0.882$, $\text{MAE} = ₹23,450.80$
* **Inference Pipeline**: Serialized into `best_sales_demand_model.joblib` with recursive multi-step autoregressive projection and 95% confidence intervals (+/- 15%).

### Backend API & React Frontend (Phase 7)
* **Dynamic Parameterized Queries**: All endpoints support multi-criteria filtering across Date range, Category, State, Status, Fulfilment, and Channel.
* **Multi-Engine Database Fallback**: Connects directly to PostgreSQL when available, with automated fallback to an in-memory SQL mirror of the processed dataset.
* **Glassmorphic UI**: Interactive dashboard built with custom CSS variables, Recharts visual canvas, active filter indicators, and responsive tab layout.

---

## 💡 4. Engineering Challenges & Solutions

| Challenge | Problem Description | Engineering Solution |
| :--- | :--- | :--- |
| **Financial Inconsistency in Raw Data** | Raw rows showed non-zero revenue for cancelled or returned orders. | Implemented a vector condition: if `Status == 'Cancelled'` or `is_returned == True`, set `Realized_Revenue = 0.0`. Validated with automated assertions. |
| **Multi-Day ML Autoregression** | When predicting 14 days ahead, ground-truth lag features (`lag_1`, `rolling_mean_7`) are not yet available for future days. | Built a recursive inference generator where each predicted step's revenue is appended to an in-memory history buffer to dynamically compute subsequent lags. |
| **Cross-Platform SQL Engine Parity** | The web application needed to run seamlessly in local developer environments even if PostgreSQL was offline. | Architected a unified `DatabaseManager` that queries PostgreSQL when online, and automatically mirrors the 128k records in an in-memory SQL database with identical schema and syntax. |
| **State Name Normalization** | Raw dataset contained 69 messy variations of 38 Indian states (e.g. `'NL'`, `'AR'`, `'PUDUCHERRY'`, `'pondicherry'`). | Created a dictionary mapping table in Python to resolve all 69 variants into official ISO/Census state names with 100% resolution. |

---

## ❓ 5. 20 Realistic Technical Interview Questions & Answers

### Q1: How did you distinguish Gross Listed Sales from Realized Net Revenue?
**Answer**: Gross listed sales reflects total consumer demand before operational attrition (`SUM(gross_amount)` = ₹78.59M). Realized net revenue recognizes cash income only for delivered or in-transit orders (`SUM(realized_revenue)` = ₹70.29M), setting cancellations and returns strictly to ₹0.00.

### Q2: What was the primary driver of the ₹8.31M unrealized revenue?
**Answer**: Pre-delivery cancellations accounted for 83.3% of the lost value (₹6.92M lost across 18,332 orders with a 14.21% cancellation rate), while post-dispatch returns contributed ₹1.38M (1.64% return rate).

### Q3: Why did you choose a Star Schema over a 3NF normalized schema for Power BI?
**Answer**: Star Schemas optimize analytical query performance in columnar OLAP engines like VertiPaq. By decoupling transactions into `Fact_AmazonSales` and surrounding it with 5 single-direction Dimension tables (`Dim_Date`, `Dim_Product`, `Dim_Geography`, `Dim_OrderStatus`, `Dim_Fulfilment`), we minimized table joins and enabled fast DAX aggregations.

### Q4: How did you ensure your ML model did not suffer from data leakage?
**Answer**: We used chronological time-based splitting (first 80% of days for training, last 20% for testing) instead of random shuffling. All lag features (`lag_1`, `lag_7`) and rolling statistics (`rolling_mean_7`) were computed strictly on historical preceding rows without looking ahead into the test window.

### Q5: Why did Gradient Boosting outperform Random Forest and Linear Regression?
**Answer**: Gradient Boosting builds sequential trees to iteratively minimize residual errors. It effectively captured non-linear interactions between day-of-week seasonality, high-volume apparel categories (*Set* and *Kurta*), and rolling 7-day demand moving averages, achieving an $R^2$ of 0.946 vs 0.882 for Linear Regression.

### Q6: How does the recursive multi-step forecasting loop work in `predict.py`?
**Answer**: For step $t+1$, the model predicts daily revenue using known historical lags. For step $t+2$, the predicted revenue from step $t+1$ is appended to the rolling buffer to synthesize `lag_1`, updating `rolling_mean_7` and calendar features for the next forward prediction.

### Q7: How did you convert predicted revenue into unit demand?
**Answer**: We calculated the historical Category Average Selling Price (ASP = Total Realized Revenue / Total Units Sold). The predicted daily revenue is divided by the category ASP to output forecasted unit requirements with non-negative constraints.

### Q8: How did you handle API request filtering across multiple optional parameters in FastAPI?
**Answer**: In `AnalyticsService._build_where_clause`, we dynamically construct parameterized SQL `WHERE` clauses matching only active filters (`category`, `state`, `status`, `start_date`, etc.) using named bind parameters (`:category`) to prevent SQL injection and ensure sub-millisecond execution.

### Q9: Why use FastAPI over Flask or Django?
**Answer**: FastAPI provides native asynchronous request handling, automatic OpenAPI/Swagger documentation generation at `/docs`, strict data validation via Pydantic v2, and high throughput with Uvicorn.

### Q10: How does the backend database fallback mechanism function?
**Answer**: `DatabaseManager` attempts a lightweight connection probe to PostgreSQL. If PostgreSQL is active, it executes queries via SQLAlchemy. If offline, it ingests `Data/Processed/amazon_sales_analytics.csv` into an in-memory indexed SQL engine, executing the exact same SQL queries with zero mock data.

### Q11: What is the significance of the Pareto 80/20 analysis in your SQL module?
**Answer**: Using cumulative window functions, we discovered that out of hundreds of garment styles, a small subset of Class A styles (like `JNE3797`, `JNE3405`, `SET383`) generate 80% of revenue, allowing inventory managers to focus 80% of working capital on high-velocity SKUs.

### Q12: How did you handle CORS in FastAPI?
**Answer**: We configured `CORSMiddleware` with configurable allowed origins from environment variables (`CORS_ORIGINS`), allowing the Vite React client (`http://localhost:5173`) to make seamless cross-origin requests during development.

### Q13: How does Amazon FBA fulfillment compare to Merchant fulfillment in your dataset?
**Answer**: Amazon FBA accounts for 69.5% of total volume (89,698 lines) and achieves a 93.14% financial realization rate with a 12.79% cancellation rate. Merchant direct fulfillment has a lower realization rate (81.14%) and higher cancellation rate (17.47%).

### Q14: How are confidence intervals calculated on the ML predictions?
**Answer**: We compute a symmetric +/- 15% uncertainty band around the point revenue prediction (`lower_bound = max(0, pred * 0.85)`, `upper_bound = pred * 1.15`), providing inventory planners with conservative and optimistic demand scenarios.

### Q15: What DAX measures did you create to evaluate revenue realization?
**Answer**: We created `[Realized Revenue] = SUM(Fact_AmazonSales[realized_revenue])`, `[Gross Listed Amount] = SUM(Fact_AmazonSales[gross_amount])`, and `[Realization Rate %] = DIVIDE([Realized Revenue], [Gross Listed Amount], 0)`.

### Q16: How did you manage React state across global filters and charts?
**Answer**: We managed centralized `FilterState` at the root `App.tsx` level. Filter changes trigger a single coordinated `Promise.all` API request that simultaneously updates KPIs, sales trends, category shares, top products, and geographic insights.

### Q17: What security precautions did you take for environment secrets?
**Answer**: We implemented `.env.example` templates, added `.env` to `.gitignore`, used `os.getenv` with default fallbacks, and conducted automated regex grep audits to ensure no passwords or API keys are committed to Git.

### Q18: What is the primary operational takeaway from your AI Business Insights engine?
**Answer**: Migrating merchant-fulfilled SKUs to Amazon FBA and introducing automated order verification protocols could recover a significant portion of the ₹6.92M lost to pre-dispatch cancellations.

### Q19: What are the current limitations of the ML forecasting model?
**Answer**: The dataset covers a 3-month snapshot (April–June 2022). Consequently, the model cannot capture full annual seasonality (e.g., Diwali or Q4 holiday shopping peaks). Predictions are most accurate for 7-to-30 day operational horizons.

### Q20: What are the next architectural steps if scaling to 10M+ rows?
**Answer**:
1. Implement Apache Kafka for real-time order stream ingestion.
2. Deploy PostgreSQL read-replicas with Redis caching for API queries.
3. Migrate the ML model to LightGBM with MLflow model registry and automated retraining pipelines.
4. Containerize backend and frontend with Docker and deploy to AWS ECS / Kubernetes.
