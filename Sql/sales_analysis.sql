-- =============================================================================
-- AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
-- PHASE 4: BUSINESS-ORIENTED SQL ANALYSIS & EXECUTIVE REPORTING
-- =============================================================================
-- Target Database: ecommerce_analytics
-- Target Table:    amazon_sales (128,975 rows)
-- Primary Currency: INR (₹)
--
-- SECTIONS:
--   1. Database & Data Validation Queries
--   2. Overall Executive Sales KPIs
--   3. Monthly Sales & Revenue Trends
--   4. Category Performance & Realization Metrics
--   5. Top Products (Styles & SKUs) Analysis
--   6. Order Status & Operational Bottlenecks
--   7. Geographic & Regional Market Analysis
--   8. Fulfilment & Logistics Channel Performance
--   9. Sales Channel Performance
--  10. Customer Segmentation (B2B vs B2C)
--  11. Average Order Value (AOV) & Basket Size Metrics
--  12. Advanced Business Insights (Window Functions, CTEs, MoM Growth, Pareto)
-- =============================================================================


-- =============================================================================
-- SECTION 1: DATABASE & DATA INTEGRITY VALIDATION
-- =============================================================================

-- 1.1 Verify total row count (Expected: 128,975)
SELECT COUNT(*) AS total_rows
FROM amazon_sales;

-- 1.2 Verify distinct order count (Expected: 120,378)
SELECT COUNT(DISTINCT order_id) AS total_unique_orders
FROM amazon_sales;

-- 1.3 Verify date range (Expected: 2022-03-31 to 2022-06-29)
SELECT 
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date,
    MAX(order_date) - MIN(order_date) AS date_span_days
FROM amazon_sales;

-- 1.4 Validate Financial Invariant: Realized Revenue <= Gross Amount (Violations must be 0)
SELECT 
    COUNT(*) AS invariant_violations,
    COALESCE(SUM(CASE WHEN realized_revenue > gross_amount THEN 1 ELSE 0 END), 0) AS violation_count
FROM amazon_sales
WHERE realized_revenue > gross_amount;

-- 1.5 Column-wise NULL verification across key analytical fields
SELECT 
    COUNT(*) - COUNT(order_id)         AS null_order_ids,
    COUNT(*) - COUNT(order_date)       AS null_order_dates,
    COUNT(*) - COUNT(status)           AS null_statuses,
    COUNT(*) - COUNT(category)         AS null_categories,
    COUNT(*) - COUNT(gross_amount)     AS null_gross_amounts,
    COUNT(*) - COUNT(realized_revenue) AS null_realized_revenues,
    COUNT(*) - COUNT(ship_state)       AS null_states
FROM amazon_sales;


-- =============================================================================
-- SECTION 2: OVERALL EXECUTIVE SALES KPIS
-- =============================================================================

-- 2.1 Core Executive KPI Scorecard
SELECT 
    COUNT(DISTINCT order_id)                                AS total_unique_orders,
    COUNT(*)                                                AS total_order_lines,
    SUM(qty)                                                AS total_units_ordered,
    COUNT(DISTINCT sku)                                     AS unique_products_sku,
    COUNT(DISTINCT category)                                AS total_categories,
    ROUND(SUM(gross_amount), 2)                             AS total_gross_listed_amount,
    ROUND(SUM(realized_revenue), 2)                         AS total_realized_net_revenue,
    ROUND(SUM(gross_amount) - SUM(realized_revenue), 2)     AS total_unrealized_lost_value,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS overall_realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS overall_cancellation_rate_pct,
    ROUND(SUM(CASE WHEN is_returned THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)  AS overall_return_rate_pct,
    ROUND(SUM(CASE WHEN has_promotion THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS promotion_usage_rate_pct,
    ROUND(AVG(gross_amount), 2)                             AS avg_gross_line_amount,
    ROUND(AVG(realized_revenue), 2)                         AS avg_realized_line_revenue
FROM amazon_sales;


-- =============================================================================
-- SECTION 3: MONTHLY SALES TRENDS & REVENUE TRAJECTORY
-- =============================================================================

-- 3.1 Monthly Performance Breakdown
SELECT 
    order_year,
    order_month,
    month_name,
    COUNT(DISTINCT order_id)                                AS monthly_orders,
    COUNT(*)                                                AS monthly_order_lines,
    SUM(qty)                                                AS monthly_quantity,
    ROUND(SUM(gross_amount), 2)                             AS monthly_gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS monthly_realized_revenue,
    ROUND(SUM(gross_amount) - SUM(realized_revenue), 2)     AS monthly_lost_value,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM amazon_sales
GROUP BY order_year, order_month, month_name
ORDER BY order_year, order_month;

-- 3.2 Month-over-Month (MoM) Growth Analysis using Window Functions (LAG)
WITH monthly_kpis AS (
    SELECT 
        order_year,
        order_month,
        month_name,
        COUNT(DISTINCT order_id) AS orders,
        SUM(realized_revenue)    AS realized_revenue
    FROM amazon_sales
    GROUP BY order_year, order_month, month_name
)
SELECT 
    order_year,
    order_month,
    month_name,
    orders,
    ROUND(realized_revenue, 2) AS realized_revenue,
    LAG(orders) OVER (ORDER BY order_year, order_month) AS prev_month_orders,
    ROUND(realized_revenue - LAG(realized_revenue) OVER (ORDER BY order_year, order_month), 2) AS revenue_growth_amount,
    ROUND((realized_revenue - LAG(realized_revenue) OVER (ORDER BY order_year, order_month)) / 
          NULLIF(LAG(realized_revenue) OVER (ORDER BY order_year, order_month), 0) * 100, 2) AS revenue_growth_pct
FROM monthly_kpis
ORDER BY order_year, order_month;


-- =============================================================================
-- SECTION 4: PRODUCT CATEGORY PERFORMANCE & REALIZATION
-- =============================================================================

-- 4.1 Comprehensive Category Performance Matrix
SELECT 
    category,
    COUNT(*)                                                AS total_transactions,
    SUM(qty)                                                AS total_quantity,
    COUNT(DISTINCT sku)                                     AS distinct_skus,
    ROUND(SUM(gross_amount), 2)                             AS total_gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS total_realized_revenue,
    ROUND(SUM(realized_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS revenue_share_pct,
    ROUND(AVG(gross_amount), 2)                             AS avg_unit_gross_price,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM amazon_sales
GROUP BY category
ORDER BY total_realized_revenue DESC;


-- =============================================================================
-- SECTION 5: TOP PRODUCTS (STYLES & SKUS)
-- =============================================================================

-- 5.1 Top 10 High-Revenue Garment Styles
SELECT 
    style,
    category,
    COUNT(*)                                                AS total_orders,
    SUM(qty)                                                AS total_quantity,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
FROM amazon_sales
GROUP BY style, category
ORDER BY realized_revenue DESC
LIMIT 10;

-- 5.2 Top 10 High-Velocity SKUs by Units Sold
SELECT 
    sku,
    style,
    category,
    size,
    COUNT(*)                        AS total_transactions,
    SUM(qty)                        AS total_units_sold,
    ROUND(SUM(realized_revenue), 2) AS realized_revenue,
    ROUND(AVG(realized_revenue), 2) AS avg_unit_realized_revenue
FROM amazon_sales
WHERE is_realized = TRUE
GROUP BY sku, style, category, size
ORDER BY total_units_sold DESC
LIMIT 10;

-- 5.3 Apparel Size Velocity Breakdown
SELECT 
    size,
    COUNT(*)                                                AS total_orders,
    SUM(qty)                                                AS total_units,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS revenue_share_pct
FROM amazon_sales
GROUP BY size
ORDER BY total_units DESC;


-- =============================================================================
-- SECTION 6: ORDER STATUS ANALYSIS & OPERATIONAL BOTTLENECKS
-- =============================================================================

-- 6.1 Order Status Granular Breakdown
SELECT 
    status,
    COUNT(*)                                                AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS status_share_pct,
    SUM(qty)                                                AS total_quantity,
    ROUND(SUM(gross_amount), 2)                             AS total_gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS total_realized_revenue,
    ROUND(AVG(gross_amount), 2)                             AS avg_order_gross_value
FROM amazon_sales
GROUP BY status
ORDER BY order_count DESC;

-- 6.2 Courier Status Distribution & Cross-Check
SELECT 
    courier_status,
    COUNT(*)                        AS total_records,
    ROUND(SUM(gross_amount), 2)     AS gross_amount,
    ROUND(SUM(realized_revenue), 2) AS realized_revenue,
    SUM(CASE WHEN is_cancelled THEN 1 ELSE 0 END) AS cancelled_count
FROM amazon_sales
GROUP BY courier_status
ORDER BY total_records DESC;


-- =============================================================================
-- SECTION 7: GEOGRAPHIC & REGIONAL MARKET ANALYSIS
-- =============================================================================

-- 7.1 Top 15 States by Realized Revenue & Market Share
SELECT 
    ship_state,
    COUNT(DISTINCT order_id)                                AS total_orders,
    COUNT(*)                                                AS total_order_lines,
    SUM(qty)                                                AS total_units,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS state_revenue_share_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
FROM amazon_sales
GROUP BY ship_state
ORDER BY realized_revenue DESC
LIMIT 15;

-- 7.2 Top 15 Metro Cities by Realized Revenue
SELECT 
    ship_city,
    ship_state,
    COUNT(DISTINCT order_id)        AS total_orders,
    SUM(qty)                        AS total_quantity,
    ROUND(SUM(realized_revenue), 2) AS total_realized_revenue,
    ROUND(AVG(realized_revenue), 2) AS avg_line_revenue
FROM amazon_sales
WHERE ship_city != 'Unknown/Not Provided' AND is_realized = TRUE
GROUP BY ship_city, ship_state
ORDER BY total_realized_revenue DESC
LIMIT 15;


-- =============================================================================
-- SECTION 8: FULFILMENT & LOGISTICS CHANNEL PERFORMANCE
-- =============================================================================

-- 8.1 Amazon FBA vs Merchant Fulfillment Comparison
SELECT 
    fulfilment,
    fulfilled_by,
    COUNT(*)                                                AS total_order_lines,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS volume_share_pct,
    SUM(qty)                                                AS total_quantity,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
    ROUND(SUM(CASE WHEN is_returned THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)  AS return_rate_pct
FROM amazon_sales
GROUP BY fulfilment, fulfilled_by
ORDER BY total_order_lines DESC;

-- 8.2 Shipping Service Speed Performance (Expedited vs Standard)
SELECT 
    ship_service_level,
    fulfilment,
    COUNT(*)                                                AS total_orders,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM amazon_sales
GROUP BY ship_service_level, fulfilment
ORDER BY total_orders DESC;


-- =============================================================================
-- SECTION 9: SALES CHANNEL PERFORMANCE
-- =============================================================================

-- 9.1 Platform Sales Channel Distribution
SELECT 
    sales_channel,
    COUNT(*)                                                AS total_records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS channel_share_pct,
    SUM(qty)                                                AS total_units,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct
FROM amazon_sales
GROUP BY sales_channel
ORDER BY total_records DESC;


-- =============================================================================
-- SECTION 10: CUSTOMER SEGMENTATION (B2B vs B2C)
-- =============================================================================

-- 10.1 Retail B2C vs Wholesale B2B Analysis
SELECT 
    CASE WHEN is_b2b THEN 'B2B (Business / GST Registered)' ELSE 'B2C (Retail Consumer)' END AS customer_segment,
    COUNT(DISTINCT order_id)                                AS total_orders,
    COUNT(*)                                                AS total_order_lines,
    SUM(qty)                                                AS total_quantity,
    ROUND(SUM(gross_amount), 2)                             AS gross_amount,
    ROUND(SUM(realized_revenue), 2)                         AS realized_revenue,
    ROUND(AVG(gross_amount), 2)                             AS avg_order_gross_value,
    ROUND(SUM(qty) * 1.0 / COUNT(DISTINCT order_id), 2)     AS avg_basket_size_units,
    ROUND(SUM(realized_revenue) / SUM(gross_amount) * 100, 2) AS realization_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM amazon_sales
GROUP BY is_b2b
ORDER BY total_orders DESC;


-- =============================================================================
-- SECTION 11: AVERAGE ORDER VALUE (AOV) & BASKET SIZE METRICS
-- =============================================================================

-- 11.1 Order-Level Basket Size & Realized Order Value
WITH order_aggregates AS (
    SELECT 
        order_id,
        order_date,
        COUNT(*)               AS items_in_order,
        SUM(qty)               AS total_units_in_order,
        SUM(gross_amount)      AS order_gross_total,
        SUM(realized_revenue)  AS order_realized_total,
        MAX(CASE WHEN is_cancelled THEN 1 ELSE 0 END) AS is_order_cancelled
    FROM amazon_sales
    GROUP BY order_id, order_date
)
SELECT 
    COUNT(*)                                            AS total_orders,
    ROUND(AVG(items_in_order), 2)                       AS avg_line_items_per_order,
    ROUND(AVG(total_units_in_order), 2)                 AS avg_units_per_order,
    ROUND(AVG(order_gross_total), 2)                    AS avg_gross_order_value_aov,
    ROUND(AVG(CASE WHEN order_realized_total > 0 THEN order_realized_total END), 2) AS avg_realized_aov_completed_orders,
    MAX(items_in_order)                                 AS max_items_in_single_order,
    ROUND(MAX(order_gross_total), 2)                    AS max_single_order_value
FROM order_aggregates;

-- 11.2 Single-Item vs Multi-Item Order Distribution
WITH order_sizes AS (
    SELECT 
        order_id,
        COUNT(*) AS item_count,
        SUM(realized_revenue) AS order_revenue
    FROM amazon_sales
    GROUP BY order_id
)
SELECT 
    CASE 
        WHEN item_count = 1 THEN '1. Single-Item Order'
        WHEN item_count = 2 THEN '2. Two-Item Order'
        WHEN item_count BETWEEN 3 AND 5 THEN '3. Medium Basket (3-5 Items)'
        ELSE '4. Large Basket (>5 Items)'
    END AS basket_size_tier,
    COUNT(*)                                            AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT order_id) FROM amazon_sales), 2) AS order_share_pct,
    ROUND(SUM(order_revenue), 2)                        AS total_revenue,
    ROUND(SUM(order_revenue) / (SELECT SUM(realized_revenue) FROM amazon_sales) * 100, 2) AS revenue_share_pct,
    ROUND(AVG(order_revenue), 2)                        AS avg_revenue_per_order
FROM order_sizes
GROUP BY 
    CASE 
        WHEN item_count = 1 THEN '1. Single-Item Order'
        WHEN item_count = 2 THEN '2. Two-Item Order'
        WHEN item_count BETWEEN 3 AND 5 THEN '3. Medium Basket (3-5 Items)'
        ELSE '4. Large Basket (>5 Items)'
    END
ORDER BY basket_size_tier;


-- =============================================================================
-- SECTION 12: ADVANCED BUSINESS INSIGHTS (CTEs, WINDOW FUNCTIONS & PARETO)
-- =============================================================================

-- 12.1 Cumulative Running Revenue & Daily Growth Trend
WITH daily_revenue_series AS (
    SELECT 
        order_date,
        COUNT(DISTINCT order_id) AS daily_orders,
        SUM(realized_revenue)    AS daily_revenue
    FROM amazon_sales
    GROUP BY order_date
)
SELECT 
    order_date,
    daily_orders,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(SUM(daily_revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_running_revenue,
    ROUND(AVG(daily_revenue) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7day_avg_revenue
FROM daily_revenue_series
ORDER BY order_date;

-- 12.2 Pareto 80/20 Analysis on Garment Styles (Which styles generate 80% of revenue?)
WITH style_revenues AS (
    SELECT 
        style,
        category,
        SUM(realized_revenue) AS style_revenue
    FROM amazon_sales
    GROUP BY style, category
),
ranked_styles AS (
    SELECT 
        style,
        category,
        style_revenue,
        SUM(style_revenue) OVER (ORDER BY style_revenue DESC) AS cumulative_style_revenue,
        SUM(style_revenue) OVER () AS grand_total_revenue
    FROM style_revenues
)
SELECT 
    style,
    category,
    ROUND(style_revenue, 2) AS style_revenue,
    ROUND(cumulative_style_revenue, 2) AS cumulative_revenue,
    ROUND(cumulative_style_revenue / grand_total_revenue * 100, 2) AS cumulative_revenue_pct,
    CASE 
        WHEN (cumulative_style_revenue / grand_total_revenue) <= 0.80 THEN 'Top 80% Revenue Driver (Class A)'
        WHEN (cumulative_style_revenue / grand_total_revenue) <= 0.95 THEN 'Next 15% Driver (Class B)'
        ELSE 'Long Tail 5% (Class C)'
    END AS pareto_classification
FROM ranked_styles
ORDER BY style_revenue DESC
LIMIT 25;

-- 12.3 Promotion Impact Assessment: Average Line Realization by Category
SELECT 
    category,
    ROUND(AVG(CASE WHEN has_promotion THEN realized_revenue END), 2)     AS avg_realized_promoted,
    ROUND(AVG(CASE WHEN NOT has_promotion THEN realized_revenue END), 2) AS avg_realized_non_promoted,
    ROUND(AVG(CASE WHEN has_promotion THEN realized_revenue END) - 
          AVG(CASE WHEN NOT has_promotion THEN realized_revenue END), 2) AS observed_difference,
    ROUND(SUM(CASE WHEN has_promotion THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS category_promo_adoption_rate_pct
FROM amazon_sales
GROUP BY category
ORDER BY category_promo_adoption_rate_pct DESC;
