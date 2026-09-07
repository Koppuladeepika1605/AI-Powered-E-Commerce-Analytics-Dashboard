# Phase 4: PostgreSQL Database & SQL Analytics Architecture

**Project:** AI-Powered E-Commerce Analytics Dashboard  
**Target Database:** `ecommerce_analytics`  
**Target Table:** `amazon_sales`  
**Dataset Source:** `Data/Processed/amazon_sales_analytics.csv` (128,975 rows × 36 columns)  
**Primary Currency:** INR (₹)  

---

## 1. Database Purpose & Overview

The PostgreSQL database integration serves as the centralized, high-performance relational analytics store for the E-Commerce Dashboard project. It enables structured SQL querying, slicing, indexing, cohort analysis, and data connectivity for downstream Business Intelligence tools (such as Power BI) and Machine Learning pipelines.

---

## 2. Table Schema (`amazon_sales`)

| Column Name | PostgreSQL Data Type | Nullable | Description / Business Meaning |
| :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR(30)` | No | Amazon 3-segment order tracking identifier. |
| `order_date` | `DATE` | No | Transaction date (`YYYY-MM-DD`). |
| `order_year` | `INTEGER` | No | Extracted calendar year (2022). |
| `order_month` | `INTEGER` | No | Extracted calendar month (3, 4, 5, 6). |
| `month_name` | `VARCHAR(20)` | No | Month name ('March', 'April', 'May', 'June'). |
| `order_week` | `INTEGER` | No | ISO calendar week number (13 to 26). |
| `order_day` | `INTEGER` | No | Calendar day of the month (1 to 31). |
| `day_name` | `VARCHAR(20)` | No | Day of the week ('Monday', 'Tuesday', ...). |
| `status` | `VARCHAR(50)` | No | Granular operational order status (13 categories). |
| `courier_status` | `VARCHAR(30)` | No | Shipping partner courier tracking status. |
| `fulfilment` | `VARCHAR(30)` | No | Fulfillment channel: `Amazon` (FBA) vs `Merchant` (FBM). |
| `fulfilled_by` | `VARCHAR(30)` | No | Merchant partner logistics (`Easy Ship` or `Not Applicable`). |
| `sales_channel` | `VARCHAR(30)` | No | Platform channel (`Amazon.in` vs `Non-Amazon`). |
| `ship_service_level` | `VARCHAR(30)` | No | Shipping delivery tier (`Expedited` vs `Standard`). |
| `category` | `VARCHAR(50)` | No | Standardized garment product category (9 types). |
| `size` | `VARCHAR(20)` | No | Standardized garment sizing code. |
| `style` | `VARCHAR(50)` | No | Garment design model code. |
| `sku` | `VARCHAR(100)` | No | Unique Stock Keeping Unit identifier. |
| `asin` | `VARCHAR(30)` | No | Amazon Standard Identification Number. |
| `qty` | `INTEGER` | No | Units ordered (0 to 15). |
| `currency` | `VARCHAR(10)` | No | Transaction currency (`INR`). |
| `recorded_amount` | `NUMERIC(10,2)` | Yes | Raw listed catalog price (retains original nulls for audit). |
| `gross_amount` | `NUMERIC(10,2)` | No | Total listed gross order value (nulls imputed with 0.00). |
| `realized_revenue` | `NUMERIC(10,2)` | No | Realized net recognized cash revenue (0.00 for cancelled/returned). |
| `ship_city` | `VARCHAR(100)` | No | Standardized destination city name. |
| `ship_state` | `VARCHAR(100)` | No | Standardized Indian State / Union Territory name. |
| `ship_postal_code` | `VARCHAR(20)` | No | Standardized 6-digit Indian PIN code text string. |
| `ship_country` | `VARCHAR(20)` | No | Destination country code (`IN`). |
| `promotion_ids` | `TEXT` | No | Applied promotional coupon campaign codes. |
| `has_promotion` | `BOOLEAN` | No | Flag indicating if promotion/coupon was applied. |
| `is_b2b` | `BOOLEAN` | No | Flag indicating Business-to-Business GST customer. |
| `is_cancelled` | `BOOLEAN` | No | Flag indicating cancelled transaction. |
| `is_delivered` | `BOOLEAN` | No | Flag indicating completed delivery to buyer. |
| `is_returned` | `BOOLEAN` | No | Flag indicating customer return or return to seller. |
| `is_realized` | `BOOLEAN` | No | Flag indicating realized revenue transaction. |
| `is_valid_pin` | `BOOLEAN` | No | Flag indicating valid 6-digit Indian PIN format. |

---

## 3. Data Loading & Ingestion Process

### Method A: Automated Python Pipeline
Run the provided automated loader script:
```bash
python Sql/load_to_postgres.py
```
*Note: Configurable via environment variables: `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.*

### Method B: Native PostgreSQL `psql` CLI
```sql
-- 1. Create database and table
psql -U postgres -d postgres -c "CREATE DATABASE ecommerce_analytics;"
psql -U postgres -d ecommerce_analytics -f Sql/schema.sql

-- 2. Ingest CSV via \copy
psql -U postgres -d ecommerce_analytics -c "\copy amazon_sales FROM 'Data/Processed/amazon_sales_analytics.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');"
```

---

## 4. SQL Analysis Structure (`Sql/sales_analysis.sql`)

The SQL analysis file is structured into **12 professional, interview-ready business sections**:

1. **Database & Data Validation:** Verifies row counts, unique orders, date spans, zero nulls, and invariant $\text{Realized\_Revenue} \le \text{Gross\_Amount}$.
2. **Overall Executive Sales KPIs:** Single-query KPI scorecard (Gross Sales, Net Realized Revenue, Realization Rate, Cancellation Rate, Return Rate, Average Order Value).
3. **Monthly Sales Trends & MoM Growth:** Month-by-month revenue trajectory and Month-over-Month (MoM) growth calculations using `LAG()` window functions.
4. **Product Category Performance:** Revenue contribution, volume share, average unit gross price, and realization rates across all 9 apparel categories.
5. **Top Products (Styles & SKUs):** Top 10 revenue-generating styles, top 10 high-velocity SKUs, and size distribution.
6. **Order Status & Operational Bottlenecks:** Granular status distribution and courier performance matrix.
7. **Geographic & Regional Market Analysis:** State revenue rankings, market share percentages, and top 15 metro revenue hubs.
8. **Fulfilment & Logistics Channel Performance:** Amazon FBA vs Merchant Easy Ship realization rates, cancellation rates, and delivery speed tiers.
9. **Sales Channel Performance:** Amazon.in vs Non-Amazon sales split.
10. **Customer Segmentation (B2B vs B2C):** Retail consumer vs GST registered business order volume, basket sizes, and AOV.
11. **Average Order Value (AOV) & Basket Size:** Order-level aggregation CTEs computing single vs multi-item order revenue contributions.
12. **Advanced Analytical Insights:** Cumulative running totals using window functions, Pareto 80/20 style classification, and promotional impact metrics.

---

## 5. Summary of SQL Business Insights

- **Total Gross Demand:** **₹78,592,678.30** across **120,378 orders** (128,975 line items).
- **Total Realized Net Cash Revenue:** **₹70,285,702.00** (89.43% realization rate).
- **Total Unrealized Leakage:** **₹8,306,976.30** (Cancellations: ₹6.92M / 14.21% | Returns: ₹1.38M / 1.64%).
- **Product Concentration:** `Set` (₹35.03M) and `Kurta` (₹19.08M) generate **77.0% of total revenue**.
- **Geographic Focus:** **Maharashtra** (17.15%), **Karnataka** (13.55%), and **Telangana** (8.80%) form the top 3 state markets; **Bengaluru** is the top city.
- **Logistics Efficiency:** **Amazon FBA** achieves a **93.14% realization rate** and lower cancellations (12.79%) vs Merchant Easy Ship (81.14% realization, 17.47% cancellations).

---

## 6. Query Verification & Reproducibility
All SQL queries in `Sql/sales_analysis.sql` were cross-validated using `Sql/validate_sql_queries.py` with **100% numerical concordance** against Phase 3 Python EDA outputs.
