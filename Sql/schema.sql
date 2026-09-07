-- =============================================================================
-- AI-POWERED E-COMMERCE ANALYTICS DASHBOARD
-- PHASE 4: POSTGRESQL DATABASE & TABLE SCHEMA DEFINITION
-- =============================================================================
-- Database: ecommerce_analytics
-- Table: amazon_sales
-- Target Data: Data/Processed/amazon_sales_analytics.csv (128,975 rows x 36 columns)
-- =============================================================================

-- 1. Create Database (Run as superuser/postgres admin if not exists)
-- CREATE DATABASE ecommerce_analytics;
-- \c ecommerce_analytics;

-- 2. Drop table if exists
DROP TABLE IF EXISTS amazon_sales CASCADE;

-- 3. Create amazon_sales Table
CREATE TABLE amazon_sales (
    order_id            VARCHAR(30)     NOT NULL,
    order_date          DATE            NOT NULL,
    order_year          INTEGER         NOT NULL,
    order_month         INTEGER         NOT NULL,
    month_name          VARCHAR(20)     NOT NULL,
    order_week          INTEGER         NOT NULL,
    order_day           INTEGER         NOT NULL,
    day_name            VARCHAR(20)     NOT NULL,
    status              VARCHAR(50)     NOT NULL,
    courier_status      VARCHAR(30)     NOT NULL,
    fulfilment          VARCHAR(30)     NOT NULL,
    fulfilled_by        VARCHAR(30)     NOT NULL,
    sales_channel       VARCHAR(30)     NOT NULL,
    ship_service_level  VARCHAR(30)     NOT NULL,
    category            VARCHAR(50)     NOT NULL,
    size                VARCHAR(20)     NOT NULL,
    style               VARCHAR(50)     NOT NULL,
    sku                 VARCHAR(100)    NOT NULL,
    asin                VARCHAR(30)     NOT NULL,
    qty                 INTEGER         NOT NULL DEFAULT 0,
    currency            VARCHAR(10)     NOT NULL DEFAULT 'INR',
    recorded_amount     NUMERIC(10,2)   NULL,
    gross_amount        NUMERIC(10,2)   NOT NULL DEFAULT 0.00,
    realized_revenue    NUMERIC(10,2)   NOT NULL DEFAULT 0.00,
    ship_city           VARCHAR(100)    NOT NULL,
    ship_state          VARCHAR(100)    NOT NULL,
    ship_postal_code    VARCHAR(20)     NOT NULL,
    ship_country        VARCHAR(20)     NOT NULL,
    promotion_ids       TEXT            NOT NULL,
    has_promotion       BOOLEAN         NOT NULL DEFAULT FALSE,
    is_b2b              BOOLEAN         NOT NULL DEFAULT FALSE,
    is_cancelled        BOOLEAN         NOT NULL DEFAULT FALSE,
    is_delivered        BOOLEAN         NOT NULL DEFAULT FALSE,
    is_returned         BOOLEAN         NOT NULL DEFAULT FALSE,
    is_realized         BOOLEAN         NOT NULL DEFAULT FALSE,
    is_valid_pin        BOOLEAN         NOT NULL DEFAULT TRUE
);

-- 4. Create Performance Indexes
CREATE INDEX idx_amazon_sales_order_id ON amazon_sales(order_id);
CREATE INDEX idx_amazon_sales_date ON amazon_sales(order_date);
CREATE INDEX idx_amazon_sales_category ON amazon_sales(category);
CREATE INDEX idx_amazon_sales_state ON amazon_sales(ship_state);
CREATE INDEX idx_amazon_sales_status ON amazon_sales(status);
CREATE INDEX idx_amazon_sales_fulfilment ON amazon_sales(fulfilment);
CREATE INDEX idx_amazon_sales_realized ON amazon_sales(is_realized);
CREATE INDEX idx_amazon_sales_cancelled ON amazon_sales(is_cancelled);

-- 5. Copy Command for psql Ingestion
-- \copy amazon_sales FROM 'Data/Processed/amazon_sales_analytics.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
