# AI-Powered E-Commerce Analytics — React Frontend Dashboard

Modern, responsive analytics web dashboard built with **React**, **TypeScript**, **Vite**, **Recharts**, and **Lucide Icons**.

---

## ✨ Features

* **Executive KPI Scorecard**: Total Realized Sales, Gross Amount, Order Volume, Units Sold, Realized AOV, Cancellation & Return rates.
* **Interactive Dynamic Filters**: Global multi-dimensional filtering across Date ranges, Apparel Categories, Shipping States, Order Statuses, Fulfilment Types, and Sales Channels.
* **Multidimensional Visual Analytics**:
  - Monthly & Daily sales trajectory and unit velocity charts (Area & Bar).
  - Category performance ranking and revenue share donut charts.
  - Top 10 Garment Styles and Top 10 SKUs leaderboard.
  - State-wise revenue leaderboard and top metro cities demand.
  - Operational lifecycle (Order Status, Amazon FBA vs Merchant fulfilment, Sales Channel).
* **Machine Learning Demand Forecast Playground**:
  - Category selector with multi-day horizon forecasting (7, 14, 21, 30 days).
  - Scenario simulation for custom promotion discount rates and wholesale B2B ratios.
  - Multi-day timeline forecast with 95% confidence intervals (+/- 15%).
  - Detailed model metadata (GradientBoostingRegressor, Test R² 0.946).
* **AI Business Intelligence & Strategy Engine**:
  - Executive health score (84/100) and strategic commercial directives.
  - Prioritized operational leak detection and actionable recommendations.
  - Ready for future LLM integration.

---

## 🛠️ Tech Stack

* **Framework**: React 19 + TypeScript
* **Build Tool**: Vite
* **Charts**: Recharts
* **Icons**: Lucide React
* **Styling**: Vanilla CSS Design System with Dark Glassmorphism, CSS Grid, and Ambient Glows

---

## 📁 Directory Structure

```text
frontend/
├── index.html                  # HTML entrypoint
├── package.json                # NPM package definitions
├── tsconfig.json               # TypeScript compiler configuration
├── vite.config.ts              # Vite dev server & backend proxy configuration
├── src/
│   ├── main.tsx                # React DOM mount point
│   ├── App.tsx                 # Master dashboard layout & tab router
│   ├── index.css               # Design system & glassmorphic styling tokens
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces for API payloads
│   ├── services/
│   │   └── api.ts              # Fetch client connecting to FastAPI REST API
│   └── components/
│       ├── Header.tsx          # Brand header, status indicator & tabs
│       ├── FilterBar.tsx       # Global analytics filter dropdowns
│       ├── KpiCards.tsx        # Executive KPI cards grid
│       ├── SalesTrendSection.tsx # Revenue and order volume trend charts
│       ├── CategorySection.tsx # Category revenue ranking & share charts
│       ├── TopProductsSection.tsx # Top 10 Styles and SKUs table
│       ├── GeographySection.tsx# State & Metro city market analysis
│       ├── OperationsSection.tsx# Order status lifecycle & FBA vs MFN
│       ├── MlForecastingSection.tsx # ML demand forecasting playground
│       └── AiInsightsSection.tsx# AI strategic observations & recommendations
```

---

## 🏃‍♂️ How to Run the Frontend

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
```
Default `VITE_API_BASE_URL` is empty, which uses Vite's built-in proxy to route `/api/*` requests to `http://localhost:8000`.

### 3. Start Local Development Server
```bash
npm run dev
```
The dashboard will be available at: `http://localhost:5173`

### 4. Build Production Bundle
```bash
npm run build
```
Production assets are generated in `frontend/dist/`.
