# Phase 3.2: Exploratory Data Analysis (EDA) — Business Insights Report

**Project:** AI-Powered E-Commerce Analytics Dashboard  
**Dataset:** `Data/Processed/amazon_sales_analytics.csv` (128,975 rows × 36 columns)  
**Date of Analysis:** September 5, 2026  
**Status:** Validated & Finalized

---

## 1. Executive Summary & Core KPIs

| KPI Metric | Value | Business Significance |
| :--- | :--- | :--- |
| **Total Unique Orders** | **120,378** | Total unique buyer shopping carts processed. |
| **Total Order Line Items** | **128,975** | 1.07 items per order average basket size. |
| **Total Units Ordered** | **116,649** | Units dispatched across Q2 2022. |
| **Total Gross Listed Amount** | **₹78,592,678.30** | Cumulative catalog gross value. |
| **Total Realized Net Revenue** | **₹70,285,702.00** | Actual realized cashflow from non-cancelled/delivered sales. |
| **Unrealized / Lost Value** | **₹8,306,976.30** | 10.57% revenue loss due to cancellations and returns. |
| **Overall Realization Rate** | **89.43%** | Proportion of listed demand converted to realized revenue. |
| **Overall Cancellation Rate** | **14.21%** | 18,332 transactions cancelled before completion. |
| **Overall Return Rate** | **1.64%** | 2,109 items returned to seller post-dispatch. |
| **Promotion Adoption Rate** | **61.89%** | 79,822 transactions had discount coupons applied. |
| **Average Line Realized Value**| **₹544.96** | Average net realized revenue generated per order line. |

---

## 2. Top 10 Strategic Business Insights

### Insight 1: Catalog Revenue Concentration in Two Hero Categories
- **Observation:** `Set` (₹35.53M / 50.55% of realized revenue) and `Kurta` (₹18.89M / 26.87% of realized revenue) collectively drive **77.42% of total realized sales**.
- **Business Implication:** The e-commerce brand operates with high product concentration risk. Supply chain prioritization and inventory stock buffers must focus primarily on high-velocity Kurta and apparel Sets.

### Insight 2: Long-Tail Categories with High Unit Economics
- **Observation:** `Western Dress` is the 3rd largest category (₹10.05M realized revenue, 14.30% share) with a premium average order value (~₹650–₹750). `Saree` (₹72.8K) and `Dupatta` (₹855) represent minor niche volume.
- **Business Implication:** Western Dress represents a scalable growth vector to diversify beyond ethnic wear.

### Insight 3: Geographic Dominance of Southern & Western Urban Hubs
- **Observation:** **Maharashtra** (₹11.96M / 17.02%) and **Karnataka** (₹9.52M / 13.54%) are the top 2 revenue-generating states, followed by **Telangana** (₹6.31M), **Uttar Pradesh** (₹5.84M), and **Tamil Nadu** (₹5.82M).
- **Top Cities:** **Bengaluru** (₹6.15M), **Hyderabad** (₹4.46M), and **Mumbai** (₹3.17M) are the top 3 metro revenue engines.
- **Business Implication:** Regional fulfillment hubs should be optimized near Bengaluru, Mumbai-Pune, and Hyderabad to support rapid 1-day/2-day delivery SLAs.

### Insight 4: High Realization Efficiency Across Core Garments
- **Observation:** The revenue realization rate is remarkably consistent across major categories: `Set` (89.52%), `Kurta` (88.75%), `Western Dress` (89.65%), `Top` (89.70%).
- **Business Implication:** No individual category suffers from abnormal cancellation or return behavior; operational friction is uniform.

### Insight 5: Cancellation Patterns & Unrealized Capital
- **Observation:** Overall cancellation rate stands at **14.21%** (18,332 line items), resulting in **₹6.92M in gross cancelled value**.
- **Business Implication:** Pre-dispatch cancellation is the single largest source of unrealized revenue. Implementing immediate order confirmation prompts and faster dispatch handoffs can mitigate buyer remorse.

### Insight 6: Return Rates are Healthy and Contained
- **Observation:** Customer returns and courier returns account for **1.64%** (2,109 items, ₹1.38M value).
- **Business Implication:** A <2% return rate is exceptionally strong for the Indian online fashion/apparel sector (where industry averages often hover between 15%–25%), indicating accurate size charts and product imagery.

### Insight 7: Fulfillment Channel Performance (FBA vs Merchant)
- **Observation:** **Amazon FBA (Fulfilled by Amazon)** accounts for **69.55% of volume** (89,698 orders, ₹49.77M realized revenue) with an **89.96% realization rate**. **Merchant Easy Ship** accounts for **30.45% of volume** (39,277 orders, ₹20.51M realized revenue) with an **88.18% realization rate**.
- **Cancellation Rates:** Amazon FBA has an observed cancellation rate of 12.87% vs Merchant Easy Ship at 17.27%.
- **Business Implication:** Orders fulfilled through Amazon FBA demonstrate 4.4% lower cancellation rates, likely due to Prime trust and faster delivery commitments.

### Insight 8: Promotion Association & Discount Penetration
- **Observation:** **61.89% of transactions** (79,822 items) utilized promotional discounts, generating **₹43.89M in realized revenue** (62.45% of total).
- **Observed Metrics:** Promoted transactions exhibited an average realized line value of **₹549.91** compared to **₹536.93** for non-promoted transactions.
- **Statistical Note:** This represents observed transactional association (promoted purchases often correspond to multi-piece sets or higher catalog value items) and does not establish causal incrementality.

### Insight 9: Monthly Sales Trajectory (April Peak & June Trough)
- **Observation:**
  - **April 2022:** 49,067 orders | ₹26.54M Realized Revenue (Peak month, 37.76% of Q2 total)
  - **May 2022:** 42,040 orders | ₹23.01M Realized Revenue
  - **June 2022:** 37,868 orders | ₹20.73M Realized Revenue (29.49% of Q2 total)
- **Business Implication:** Sales experienced an 21.9% contraction between April and June, coinciding with post-festival seasonal demand normalization.

### Insight 10: High B2C Orientation with Emerging B2B Channel
- **Observation:** Retail B2C orders represent **99.32%** of volume. B2B orders represent **0.68%** (871 orders), generating **₹599.7K in realized revenue**.
- **Business Implication:** The B2B GST merchant segment has higher average order quantities and represents an untapped channel for bulk wholesale distribution.

---

## 3. Core Recommendations for SQL, BI, and ML Modeling

1. **SQL Analytics Focus:** Write optimized aggregation queries for State-Category performance matrices, monthly cohort realization trends, and fulfillment channel efficiency.
2. **Power BI Dashboard Layout:**
   - *Executive View:* KPI Cards (Revenue, Realization Rate, Cancellation Rate), Monthly Trend, Category Share.
   - *Geographic View:* Indian State Shape Map with Revenue Heatmap and City Drill-down.
   - *Product & Inventory View:* Category & Size distribution, SKU velocity.
   - *Logistics & Returns View:* FBA vs Merchant comparison, Courier Status breakdown.
3. **Machine Learning Candidates:**
   - *Order Cancellation Predictor:* Classification model predicting likelihood of cancellation based on Category, Amount, State, Fulfillment, and Promotion.
   - *Sales Demand Forecasting:* Time-series forecasting for daily/weekly order volumes.

---
*Generated automatically by EDA pipeline in Analysis/03_eda.py.*
