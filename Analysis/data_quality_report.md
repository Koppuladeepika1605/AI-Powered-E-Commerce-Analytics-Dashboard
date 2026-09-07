# Phase 1: Data Understanding & Data Quality Report

**Project:** AI-Ecommerce-Analytics-Dashboard  
**Dataset:** Amazon Sales Report  
**Location:** `Data/Raw Data/amazon_sales.csv.csv`  
**Date of Audit:** September 5, 2026  
**Status:** Complete — Read-Only Inspection (No data modified)

---

## 1. Executive Summary

This report provides a comprehensive data audit and quality assessment of the Amazon Sales Report dataset for the **AI E-Commerce Analytics Dashboard** project. The dataset captures transactional e-commerce sales records across various apparel categories in India over a 3-month period (April 2022 to June 2022).

| Metric | Value |
| :--- | :--- |
| **File Name** | `amazon_sales.csv.csv` |
| **File Path** | `Data/Raw Data/amazon_sales.csv.csv` |
| **File Size** | ~68.9 MB (68,923,428 bytes) |
| **Total Rows** | 128,975 |
| **Total Columns** | 24 |
| **Memory Usage** | ~23.6 MB (in-memory uncompressed DataFrame) |
| **Date Range** | March 31, 2022 – June 29, 2022 (Q2 2022) |
| **Unique Orders** | 120,378 |
| **Full Duplicate Rows** | 0 (0.00%) |
| **Data Integrity Score** | **Medium-High (78/100)** — Clean transactional IDs and core categories, but requires structured handling for cancellations, currency/amount nulls, trailing column whitespaces, and state name standardization. |

---

## 2. Dataset Schema & Overview

The raw dataset consists of 24 columns representing order identifiers, transaction dates, fulfillment modes, product details, shipment destinations, and order financial values.

| # | Column Name | Raw Data Type | Recommended Type | Non-Null Count | Null Count | Null % | Description / Purpose |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | `index` | `int64` | `int64` (Drop/Ignore) | 128,975 | 0 | 0.00% | Row sequence index from export (redundant). |
| 1 | `Order ID` | `object` (string) | `string` | 128,975 | 0 | 0.00% | Unique 3-part Amazon order tracking identifier. |
| 2 | `Date` | `object` (string) | `datetime64[ns]` | 128,975 | 0 | 0.00% | Transaction date formatted as `MM-DD-YY`. |
| 3 | `Status` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Detailed operational status of the order. |
| 4 | `Fulfilment` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Fulfillment method (`Amazon` vs `Merchant`). |
| 5 | `Sales Channel ` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Platform channel (`Amazon.in` vs `Non-Amazon`). Note trailing space! |
| 6 | `ship-service-level` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Shipping speed (`Expedited` vs `Standard`). |
| 7 | `Style` | `object` (string) | `string` | 128,975 | 0 | 0.00% | Product design code (e.g., `SET389`, `JNE3781`). |
| 8 | `SKU` | `object` (string) | `string` | 128,975 | 0 | 0.00% | Stock Keeping Unit (style + color/variant + size). |
| 9 | `Category` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Product garment type (e.g., `Set`, `kurta`, `Western Dress`). |
| 10 | `Size` | `object` (string) | `category` | 128,975 | 0 | 0.00% | Garment sizing code (`S`, `M`, `L`, `XL`, `XXL`, `3XL`, etc.). |
| 11 | `ASIN` | `object` (string) | `string` | 128,975 | 0 | 0.00% | Amazon Standard Identification Number (10 alphanumeric chars). |
| 12 | `Courier Status` | `object` (string) | `category` | 122,103 | 6,872 | 5.33% | Status reported by shipping partner (`Shipped`, `Unshipped`, `Cancelled`). |
| 13 | `Qty` | `int64` | `int32` | 128,975 | 0 | 0.00% | Quantity of units ordered (0 to 15). |
| 14 | `currency` | `object` (string) | `category` | 121,180 | 7,795 | 6.04% | Transaction currency code (`INR`). |
| 15 | `Amount` | `float64` | `float64` | 121,180 | 7,795 | 6.04% | Net order value in INR (₹0.00 to ₹5,584.00). |
| 16 | `ship-city` | `object` (string) | `string` | 128,942 | 33 | 0.03% | Delivery destination city name. |
| 17 | `ship-state` | `object` (string) | `string` | 128,942 | 33 | 0.03% | Delivery destination Indian state / UT. |
| 18 | `ship-postal-code` | `float64` | `string` / `Int64` | 128,942 | 33 | 0.03% | Delivery 6-digit Indian PIN code. |
| 19 | `ship-country` | `object` (string) | `category` | 128,942 | 33 | 0.03% | Delivery destination country (`IN`). |
| 20 | `promotion-ids` | `object` (string) | `string` | 79,822 | 49,153 | 38.11% | Comma-separated Amazon promotion & coupon campaign codes. |
| 21 | `B2B` | `bool` | `bool` | 128,975 | 0 | 0.00% | Flag indicating Business-to-Business (GST registered) order. |
| 22 | `fulfilled-by` | `object` (string) | `category` | 39,277 | 89,698 | 69.55% | Merchant logistics mechanism (`Easy Ship` when Fulfilment=Merchant). |
| 23 | `Unnamed: 22` | `object` (boolean/str) | Drop | 79,925 | 49,050 | 38.03% | Unlabelled boolean column (`False` or `NaN`), artifacts of export. |

---

## 3. Data Dictionary

Detailed functional definitions for business and engineering contexts:

### 3.1 Order Identification & Timing
- **`Order ID`**: Standard 3-segment Amazon tracking identifier (format `XXX-XXXXXXX-XXXXXXX`). An order can have multiple rows when the customer buys multiple items.
- **`Date`**: The timestamp the customer placed the order, ranging between March 31, 2022 and June 29, 2022.

### 3.2 Logistics & Fulfillment Channels
- **`Fulfilment`**: Fulfillment method used.
  - `Amazon` (FBA - Fulfilled by Amazon): 89,698 orders (69.55%). Handled directly by Amazon fulfillment centers.
  - `Merchant` (FBM - Fulfilled by Merchant): 39,277 orders (30.45%). Stocked by merchant, shipped via Amazon Easy Ship.
- **`fulfilled-by`**: Specifically denotes merchant fulfillment logistics (`Easy Ship`). Missing for all Amazon FBA orders.
- **`Sales Channel `**: Platform channel. `Amazon.in` represents 99.90% (128,851 rows), with 124 non-Amazon records.
- **`ship-service-level`**: Delivery velocity tier. `Expedited` (68.71%) vs `Standard` (31.29%).

### 3.3 Product Catalog Attributes
- **`Category`**: 9 apparel product categories:
  - `Set`: 50,284 (38.99%)
  - `kurta`: 49,877 (38.67%)
  - `Western Dress`: 15,500 (12.02%)
  - `Top`: 10,622 (8.24%)
  - `Ethnic Dress`: 1,159 (0.90%)
  - `Blouse`: 926 (0.72%)
  - `Bottom`: 440 (0.34%)
  - `Saree`: 164 (0.13%)
  - `Dupatta`: 3 (<0.01%)
- **`Size`**: Sizing codes: `M` (17.61%), `L` (17.16%), `XL` (16.19%), `XXL` (14.03%), `S` (13.25%), `3XL` (11.49%), `XS` (8.65%), `6XL` (0.57%), `5XL` (0.43%), `4XL` (0.33%), `Free` (0.29%).
- **`Style`**: 1,377 unique internal design identifiers.
- **`SKU`**: 7,195 unique Stock Keeping Units.
- **`ASIN`**: 7,190 unique Amazon Standard Identification Numbers.

### 3.4 Order Financials & Quantities
- **`Qty`**: Number of units ordered. Defaults to 1 for 89.77% of records. Rows with `Qty = 0` (12,807 rows) predominantly represent cancelled orders.
- **`currency`**: INR (Indian Rupee). Missing whenever `Amount` is missing.
- **`Amount`**: Transaction revenue value in INR. Min ₹0, Max ₹5,584, Mean ₹648.56, Median ₹605.00.
- **`B2B`**: `False` (128,104 / 99.32%) for Retail B2C orders; `True` (871 / 0.68%) for Business B2B orders.
- **`promotion-ids`**: Comma-separated list of promotional discount campaign IDs applied to the purchase.

### 3.5 Customer Geography
- **`ship-city`**: 8,956 unique delivery destination cities (top: Bengaluru, Hyderabad, Mumbai, New Delhi, Chennai).
- **`ship-state`**: 69 raw variations representing 28 States and 8 Union Territories in India.
- **`ship-postal-code`**: 6-digit Indian PIN codes (e.g. 560001, 110001, 400001).
- **`ship-country`**: `IN` (India).

---

## 4. Missing Value Analysis

| Column | Missing Count | Missing Pct (%) | Root Cause / Nature of Missingness | Action Required in Phase 2 |
| :--- | :--- | :--- | :--- | :--- |
| `fulfilled-by` | 89,698 | 69.55% | Structural: Only populated (`Easy Ship`) when `Fulfilment == 'Merchant'`. Missing for FBA. | Impute with `'Amazon'` or retain as fulfillment metadata. |
| `promotion-ids` | 49,153 | 38.11% | Business: Orders where no coupon or promo discount was applied. | Impute with `'None'` / `'No Promotion'`. |
| `Unnamed: 22` | 49,050 | 38.03% | Unnamed artifact column with only `False` or `NaN`. | Safe to drop in Phase 2. |
| `Amount` | 7,795 | 6.04% | 7,566 cancelled orders + 229 unfulfilled/shipped anomalies lacking billing records. | Impute 0.0 for cancellations; handle per business rule. |
| `currency` | 7,795 | 6.04% | Exact 1:1 match with `Amount` nulls. | Impute `'INR'` where applicable. |
| `Courier Status` | 6,872 | 5.33% | Occurs exclusively in Cancelled orders where package was never handed to courier. | Impute `'Unassigned'` / `'Cancelled'`. |
| `ship-city` | 33 | 0.03% | Missing address line in raw order dump. | Impute `'Unknown'` or infer from PIN code if possible. |
| `ship-state` | 33 | 0.03% | Exact same 33 rows as `ship-city`. | Impute `'Unknown'`. |
| `ship-postal-code`| 33 | 0.03% | Exact same 33 rows as `ship-city`. | Impute `0` or `'Unknown'`. |
| `ship-country` | 33 | 0.03% | Exact same 33 rows as `ship-city`. | Impute `'IN'`. |

---

## 5. Duplicate Rows & Granularity Audit

- **Full Exact Duplicate Rows (across all 24 columns):** **0 (0.00%)**
- **Unique `Order ID` Count:** **120,378**
- **Multi-Item Orders:**
  - Single-item orders (`count = 1`): 113,532 orders (94.31%)
  - Multi-item orders (`count > 1`): 6,846 orders (5.69%)
  - Maximum items in a single order: 12 line items
- **Conclusion:** The dataset granularity is at the **Order Line-Item level** (one row per SKU purchased per Order ID).

---

## 6. Numerical Variables & Outlier Detection

### 6.1 Descriptive Statistics
| Metric | `Qty` | `Amount` (₹) | `ship-postal-code` |
| :--- | :--- | :--- | :--- |
| **Count** | 128,975 | 121,180 | 128,942 |
| **Mean** | 0.904 | ₹648.56 | 463,966.24 |
| **Std Dev** | 0.313 | ₹281.21 | 191,476.76 |
| **Min** | 0 | ₹0.00 | 110,001 |
| **25% (Q1)** | 1 | ₹449.00 | 382,421 |
| **50% (Median)**| 1 | ₹605.00 | 500,033 |
| **75% (Q3)** | 1 | ₹788.00 | 600,024 |
| **95%** | 1 | ₹1,176.00 | 769,004 |
| **99%** | 1 | ₹1,442.00 | 834,001 |
| **Max** | 15 | ₹5,584.00 | 989,898 |

### 6.2 Outlier Analysis & Evaluation
- **`Qty` Outliers:**
  - 12,807 rows have `Qty = 0` (9.93%), directly associated with cancelled transactions.
  - 387 rows have `Qty >= 2` (max 15). These are valid bulk retail or B2B multi-piece orders, not erroneous data entry.
- **`Amount` Outliers:**
  - IQR Method (`Q1 - 1.5*IQR` to `Q3 + 1.5*IQR`): `[-59.5, 1296.5]`.
  - 3,600 rows (2.79%) have `Amount > ₹1,296.50` up to `₹5,584.00`.
  - High amounts correspond to multi-piece heavy apparel sets (e.g. premium Kurta & Palazzo sets, Silk Sarees) or bulk quantities (`Qty >= 2`). These are legitimate high-value transactions.
  - 2,343 rows have `Amount = ₹0.00` (100% discount promotional items, replacements, or sample items).

---

## 7. Suspicious, Inconsistent & Anomalous Patterns

1. **Trailing Space in Column Header:**
   - Column `Sales Channel ` contains a trailing whitespace. Needs stripping to `Sales Channel`.
2. **State Name Casing and Spelling Inconsistencies:**
   - Raw dataset has **69 unique state strings** for 36 Indian States/UTs.
   - Examples of inconsistency:
     - `MAHARASHTRA` vs `Maharashtra`
     - `DELHI` vs `Delhi` vs `New Delhi`
     - `PUDUCHERRY` vs `Pondicherry`
     - Abbreviations: `NL` (Nagaland), `AR` (Arunachal Pradesh), `PB` (Punjab), `RJ` (Rajasthan), `APO` (Army Post Office).
     - Trailing whitespace: `'ANDAMAN & NICOBAR '`.
3. **`Qty = 0` vs `Amount > 0` Discrepancy:**
   - There are 5,136 cancelled orders where `Qty == 0` but an `Amount` (e.g. ₹647.62) is listed. In e-commerce reporting, cancelled orders should reflect ₹0 net realized revenue.
4. **`Amount = ₹0` for Shipped Items:**
   - 2,234 shipped/delivered orders have `Amount = ₹0.00`, representing promotional giveaways or zero-cost replacements.
5. **Postal Codes Stored as Floats:**
   - `ship-postal-code` is stored as `float64` (e.g. `560085.0`), causing formatting issues (e.g. leading zeros lost if cast directly to int, or trailing `.0` in string exports).
6. **Redundant Artifact Columns:**
   - `index`: Simple range index duplicate.
   - `Unnamed: 22`: Export artifact with 38.03% nulls and only `False` values.

---

## 8. Recommendations for Phase 2 (Data Cleaning)

1. **Standardize Column Headers:** Strip leading/trailing whitespaces (e.g. `'Sales Channel '` $\rightarrow$ `'Sales Channel'`) and convert to snake_case.
2. **Drop Redundant Columns:** Remove `index` and `Unnamed: 22`.
3. **Parse & Format Dates:** Convert `Date` column from string `MM-DD-YY` to `datetime64[ns]` and extract `Year`, `Month`, `Month_Name`, `Day_of_Week`, and `Week_Number`.
4. **Clean & Standardize Geography:**
   - Clean state names by trimming, converting to uppercase, and mapping abbreviations (`NL` $\rightarrow$ `NAGALAND`, `AR` $\rightarrow$ `ARUNACHAL PRADESH`, `New Delhi` $\rightarrow$ `DELHI`).
   - Format `ship-postal-code` as clean 6-digit zero-padded strings.
5. **Harmonize Order Financials & Cancellations:**
   - Create a clean revenue metric (`Net_Sales_Amount`): set to 0 when status is `'Cancelled'`.
   - Maintain original gross listed amount for demand and cancellation loss analytics.
6. **Handle Missing Values Explicitly:**
   - Impute `Courier Status` missing values with `'Unassigned'`.
   - Impute `promotion-ids` missing values with `'No Promotion'`.
   - Impute `fulfilled-by` missing values with `'Amazon FBA'`.
   - Impute 33 missing customer location records with `'Unknown'`.

---
*Report generated and validated for Phase 1 Data Understanding.*
