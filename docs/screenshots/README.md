# Project Screenshots & Visual Evidence Catalog

This directory hosts visual artifacts, charts, and dashboards demonstrating the end-to-end functionality of the **AI-Powered E-Commerce Analytics Dashboard**.

---

## 📸 Catalog of Visual Assets

### 1. Machine Learning & Predictive Modeling (`docs/screenshots/`)
* **`actual_vs_predicted.png`**: Test set regression scatter plot for the Gradient Boosting Regressor ($R^2 = 0.946$, $\text{MAE} = ₹14,205.50$).
* **`feature_importance.png`**: Top 15 feature importance ranking (Leading features: `rolling_mean_7`, `lag_1`, `cat_Set`, `cat_Kurta`).
* **`daily_sales_forecast_plot.png`**: 14-day forward recursive sales & demand projection with historical baseline.

### 2. Exploratory Data Analysis & Business Intelligence
* **`monthly_revenue_trend.png`**: Monthly revenue trajectory comparing Gross Demand vs Realized Net Revenue.
* **`category_revenue.png`**: Category sales leaderboard showing Set & Kurta driving 82% of catalog revenue.
* **`top_states_revenue.png`**: Regional market penetration (Maharashtra, Karnataka, Telangana driving ~40% share).

---

## 🖥️ Live React Web Dashboard & Power BI Capture Guide

To capture live application screenshots for your resume or portfolio:

### 1. React Web Dashboard (`http://localhost:5173`)
1. Run backend: `uvicorn backend.main:app --reload`
2. Run frontend: `npm run dev` (inside `frontend/`)
3. Open `http://localhost:5173` in your browser.
4. Capture screenshots of:
   - **Executive Overview Tab**: 5 KPI cards, interactive date/category filters, sales trend chart.
   - **ML Demand Forecaster Tab**: Interactive horizon slider, category dropdown, 14-day prediction chart with confidence intervals.
   - **AI Business Insights Tab**: Executive health score, commercial win badges, and actionable directives.
5. Save screenshots into `docs/screenshots/react_dashboard_overview.png`, `docs/screenshots/react_dashboard_ml.png`, etc.

### 2. FastAPI Swagger UI (`http://localhost:8000/docs`)
1. Navigate to `http://localhost:8000/docs`.
2. Expand `/api/predictions` or `/api/kpis` with live response payload.
3. Save screenshot into `docs/screenshots/fastapi_swagger_docs.png`.

### 3. Power BI Desktop (`Dashboard/Amazon_Ecommerce_Analytics_Dashboard.pbix`)
1. Open the `.pbix` file in Power BI Desktop.
2. Capture views of Page 1 (Executive Summary), Page 2 (Product & Regional Analysis), and Page 3 (Operational Performance).
3. Save into `docs/screenshots/powerbi_overview.png`.
