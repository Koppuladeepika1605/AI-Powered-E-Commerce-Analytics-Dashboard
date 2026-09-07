# Phase 2: Data Cleaning & Preprocessing Report

**Project:** AI-Ecommerce-Analytics-Dashboard  
**Raw Dataset:** `Data/Raw Data/amazon_sales.csv.csv` *(Untouched & Preserved)*  
**Processed Datasets:** 
- [`Data/Processed/amazon_sales_cleaned.csv`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Data/Processed/amazon_sales_cleaned.csv)
- [`Data/Processed/amazon_sales_analytics.csv`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Data/Processed/amazon_sales_analytics.csv)  
**Date of Execution:** September 5, 2026  
**Status:** **Phase 2 Complete — Validated & Reproducible**

---

## 1. Executive Summary

Phase 2 established a fully reproducible, automated cleaning and feature engineering pipeline ([`Analysis/02_data_cleaning.py`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Analysis/02_data_cleaning.py)) that standardizes the raw Amazon Sales Report into a high-integrity, analytics-ready dataset. 

All **128,975 original transaction rows** were preserved without data loss. Uninformative export artifacts were removed, dates and postal codes were formatted, text and regional variations were normalized across 69 state entries, and business-accurate revenue metrics were engineered.

| Metric | Before Cleaning (Raw) | After Cleaning (Cleaned) | After Cleaning (Analytics) |
| :--- | :--- | :--- | :--- |
| **Row Count** | 128,975 | **128,975** (100% retained) | **128,975** (100% retained) |
| **Column Count** | 24 | **37** | **36** |
| **Artifact Columns** | 2 (`index`, `Unnamed: 22`) | 0 (Removed) | 0 (Removed) |
| **Derived Temporal Columns** | 0 | 6 (`Year`, `Month`, `Month_Name`, `Week`, `Day`, `Day_Name`) | 6 |
| **Business Flags & Metrics** | 0 | 9 (`Gross_Amount`, `Realized_Revenue`, `Is_Realized`, `Is_Cancelled`, `Is_Delivered`, `Is_Returned`, `Is_B2B`, `Has_Promotion`, `Is_Valid_PIN`) | 8 |
| **Total Gross Amount** | ₹78,592,678.30 | ₹78,592,678.30 | ₹78,592,678.30 |
| **Realized Net Revenue** | Undefined | **₹70,285,702.00** | **₹70,285,702.00** |
| **Unrealized / Cancelled Value**| Undefined | **₹8,306,976.30** | **₹8,306,976.30** |

---

## 2. Column Inventory & Transformations

### 2.1 Columns Removed
1. **`index`**: Raw sequence index redundant with DataFrame indexing.
2. **`Unnamed: 22`**: CSV export artifact containing 38.03% nulls and only `False` values.

### 2.2 Column Renaming & Header Normalization
- Stripped leading/trailing whitespaces across all column headers (e.g. `'Sales Channel '` $\rightarrow$ `'Sales_Channel'`).
- Renamed all columns to PascalCase / snake_case format for consistency in SQL, BI tools, and Python.

### 2.3 Columns Added / Derived
- **Temporal Dimensions:** `Year`, `Month`, `Month_Name`, `Week`, `Day`, `Day_Name`.
- **Financial Metrics:** `Gross_Amount`, `Realized_Revenue`.
- **Analytics Flags:** `Is_Realized`, `Is_Cancelled`, `Is_Delivered`, `Is_Returned`, `Is_B2B`, `Has_Promotion`, `Is_Valid_PIN`.

---

## 3. Data Type Transformations

| Column Name | Raw Type | Clean Type | Transformation & Validation Method |
| :--- | :--- | :--- | :--- |
| `Date` | `object` (string) | `datetime64[ns]` | Parsed with `pd.to_datetime(..., format='%m-%d-%y')`. 0 invalid dates. |
| `Qty` | `int64` | `int32` | Cast to 32-bit integer. |
| `Recorded_Amount` | `float64` | `float64` | Retained as continuous float with 2 decimal places. |
| `Gross_Amount` | *New* | `float64` | Imputed missing amounts with `0.0`. |
| `Realized_Revenue` | *New* | `float64` | Computed based on business fulfillment rules. |
| `Ship_Postal_Code` | `float64` | `string` | Converted from float (`400081.0`) to 6-digit text string (`'400081'`), `'UNKNOWN'` for nulls. |
| `B2B` | `bool` | `bool` | Verified boolean dtype. |
| `Category` | `object` | `string` | Trimmed and title-cased (`'kurta'` $\rightarrow$ `'Kurta'`). |
| `Size` | `object` | `string` | Trimmed and uppercase standardized. |
| `Status` | `object` | `string` | Trimmed whitespace. |
| `Ship_City` | `object` | `string` | Trimmed and title-cased; missing filled with `'Unknown/Not Provided'`. |
| `Ship_State` | `object` | `string` | Mapped using standardized 38-state dictionary. |
| `Ship_Country` | `object` | `string` | Standardized to `'IN'`. |
| `Is_Valid_PIN` | *New* | `bool` | Regex validation against Indian postal PIN pattern `^[1-9][0-9]{5}$`. |

---

## 4. Missing Value Treatment: Before vs After

| Column Name | Missing Before | % Before | Imputation / Cleaning Strategy | Missing After | % After |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Fulfilled_By` | 89,698 | 69.55% | Structural missingness for Amazon FBA. Imputed with `'Not Applicable'`. | **0** | **0.00%** |
| `Promotion_IDs` | 49,153 | 38.11% | Business missingness (no promo code). Imputed with `'No Promotion'`. | **0** | **0.00%** |
| `Courier_Status` | 6,872 | 5.33% | Unassigned orders (mostly cancelled). Imputed with `'Unassigned'`. | **0** | **0.00%** |
| `Recorded_Amount` | 7,795 | 6.04% | Retained as NaN in raw audit column; filled with `0.0` in `Gross_Amount`. | 7,795 | 6.04% |
| `Gross_Amount` | *New* | — | Directly populated from `Recorded_Amount.fillna(0.0)`. | **0** | **0.00%** |
| `Realized_Revenue`| *New* | — | Realized net revenue computed per business rule. | **0** | **0.00%** |
| `Currency` | 7,795 | 6.04% | Imputed with `'INR'`. | **0** | **0.00%** |
| `Ship_City` | 33 | 0.03% | Imputed with `'Unknown/Not Provided'`. | **0** | **0.00%** |
| `Ship_State` | 33 | 0.03% | Imputed with `'Unknown/Not Provided'`. | **0** | **0.00%** |
| `Ship_Postal_Code`| 33 | 0.03% | Imputed with `'UNKNOWN'`; flagged with `Is_Valid_PIN = False`. | **0** | **0.00%** |
| `Ship_Country` | 33 | 0.03% | Imputed with `'Unknown/Not Provided'`. | **0** | **0.00%** |

---

## 5. Comprehensive State Standardization Dictionary

All 69 raw state variations were mapped to 36 Indian States/UTs, 1 overseas/military APO, and 1 unknown category:

| Standardized State / Territory | Raw Variations Mapped | Count |
| :--- | :--- | :--- |
| **Maharashtra** | `MAHARASHTRA` | 22,260 |
| **Karnataka** | `KARNATAKA` | 17,326 |
| **Tamil Nadu** | `TAMIL NADU` | 11,483 |
| **Telangana** | `TELANGANA` | 11,330 |
| **Uttar Pradesh** | `UTTAR PRADESH` | 10,638 |
| **Delhi** | `DELHI`, `Delhi`, `delhi`, `New Delhi` | 7,048 |
| **Kerala** | `KERALA` | 6,585 |
| **West Bengal** | `WEST BENGAL` | 5,963 |
| **Andhra Pradesh** | `ANDHRA PRADESH` | 5,430 |
| **Gujarat** | `Gujarat` | 4,489 |
| **Haryana** | `HARYANA` | 4,415 |
| **Rajasthan** | `RAJASTHAN`, `Rajasthan`, `rajasthan`, `Rajshthan`, `rajsthan`, `Rajsthan`, `RJ` | 2,718 |
| **Madhya Pradesh** | `MADHYA PRADESH` | 2,529 |
| **Odisha** | `ODISHA`, `Odisha`, `Orissa`, `orissa` | 2,139 |
| **Bihar** | `BIHAR`, `Bihar`, `bihar` | 2,114 |
| **Punjab** | `PUNJAB`, `Punjab`, `punjab`, `Punjab/Mohali/Zirakpur`, `PB` | 1,919 |
| **Assam** | `ASSAM` | 1,663 |
| **Uttarakhand** | `UTTARAKHAND` | 1,553 |
| **Jharkhand** | `JHARKHAND` | 1,456 |
| **Goa** | `GOA`, `Goa`, `goa` | 1,137 |
| **Chhattisgarh** | `CHHATTISGARH` | 909 |
| **Himachal Pradesh** | `HIMACHAL PRADESH` | 788 |
| **Jammu and Kashmir** | `JAMMU & KASHMIR` | 702 |
| **Puducherry** | `PUDUCHERRY`, `Puducherry`, `Pondicherry` | 351 |
| **Chandigarh** | `CHANDIGARH`, `Chandigarh` | 333 |
| **Manipur** | `MANIPUR`, `Manipur` | 316 |
| **Andaman and Nicobar Islands** | `ANDAMAN & NICOBAR ` | 257 |
| **Meghalaya** | `MEGHALAYA`, `Meghalaya` | 207 |
| **Sikkim** | `SIKKIM`, `Sikkim` | 205 |
| **Nagaland** | `NAGALAND`, `Nagaland`, `NL` | 187 |
| **Tripura** | `TRIPURA` | 151 |
| **Arunachal Pradesh** | `ARUNACHAL PRADESH`, `Arunachal Pradesh`, `Arunachal pradesh`, `AR` | 147 |
| **Mizoram** | `MIZORAM`, `Mizoram` | 76 |
| **Dadra and Nagar Haveli and Daman and Diu** | `DADRA AND NAGAR` | 70 |
| **Ladakh** | `LADAKH` | 43 |
| **Lakshadweep** | `LAKSHADWEEP` | 4 |
| **Unknown/Other** | `APO` (Army Post Office / Overseas Military Mail) | 1 |
| **Unknown/Not Provided** | `NaN` (Missing address records) | 33 |

---

## 6. Revenue & Financial Logic

### 6.1 The Realized Revenue Business Rule
In raw e-commerce data, cancelled and returned transactions often retain their catalog list amount. Treating these as realized sales distorts GMV and revenue analytics.

$$\text{Realized\_Revenue} = \begin{cases} 
\text{Gross\_Amount} & \text{if } \text{Status} \notin \text{Non-Realized Statuses} \land \text{Qty} > 0 \land \text{Gross\_Amount} > 0 \\
0.0 & \text{otherwise}
\end{cases}$$

**Non-Realized Statuses:**
- `Cancelled` (18,332 rows, ₹6,919,284.30)
- `Shipped - Returned to Seller` (1,953 rows, ₹1,269,644.00)
- `Shipped - Returning to Seller` (145 rows, ₹107,620.00)
- `Shipped - Rejected by Buyer` (11 rows, ₹7,295.00)
- `Shipped - Lost in Transit` (5 rows, ₹1,997.00)
- `Shipped - Damaged` (1 row, ₹1,136.00)
- `Shipping` (8 rows, ₹0.00)

**Financial Summary:**
- **Gross Recorded Listed Value:** **₹78,592,678.30**
- **Realized Realized Net Revenue:** **₹70,285,702.00** (89.43%)
- **Cancellations & Returns Loss:** **₹8,306,976.30** (10.57%)

---

## 7. Special Treatments: Qty = 0, Duplicates & Outliers

### 7.1 Treatment of `Qty = 0`
- **Count:** 12,807 records (9.93% of dataset).
- **Finding:** 12,701 (99.17%) are `Cancelled` orders. 5,136 had residual listed amounts.
- **Action Taken:** Preserved all 12,807 rows to maintain transaction history for cancellation analysis. Set `Realized_Revenue = 0.0`.

### 7.2 Treatment of Duplicates
- **Full Duplicates:** 0 exact duplicates existed across all 24 columns.
- **Multi-Item Orders:** 8,597 duplicate `Order ID` entries represent legitimate multi-line orders (6,846 orders with 2 to 12 items). All rows preserved intact.

### 7.3 Treatment of Outliers
- **High Amounts (₹1,296.50 – ₹5,584.00):** Investigated against SKU, Category, and Qty. These are valid multi-piece designer sets (Kurta-Palazzo-Dupatta sets, Sarees) and multi-unit purchases. None were deleted.

---

## 8. Validation & Quality Checks

The pipeline executed automated assertions with 100% pass rate:
- [x] **Zero Row Loss:** Raw count (128,975) == Processed count (128,975).
- [x] **Zero Nulls in Core Dimensions:** `Order_ID`, `Date`, `Status`, `Category`, `Size`, `Ship_State`, `Gross_Amount`, `Realized_Revenue` have 0 nulls.
- [x] **Date Format Integrity:** `Date` is strictly valid `datetime64[ns]`.
- [x] **Postal Code Text Integrity:** `Ship_Postal_Code` is clean 6-digit text (`'400081'`), 99.97% valid PIN format.
- [x] **State Standardization:** All 69 variations mapped cleanly.
- [x] **Financial Invariant:** `Realized_Revenue <= Gross_Amount` holds universally across all 128,975 rows.
- [x] **Raw CSV Immutability:** `Data/Raw Data/amazon_sales.csv.csv` remains 100% unmodified.

---

## 9. Output Files Created

1. [`Analysis/02_data_cleaning.py`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Analysis/02_data_cleaning.py): Production-ready Python pipeline script.
2. [`Analysis/02_data_cleaning.ipynb`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Analysis/02_data_cleaning.ipynb): Interactive Jupyter notebook documenting transformations step-by-step.
3. [`Analysis/data_cleaning_report.md`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Analysis/data_cleaning_report.md): Formal data cleaning report and data governance audit.
4. [`Data/Processed/amazon_sales_cleaned.csv`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Data/Processed/amazon_sales_cleaned.csv): Complete cleaned dataset with all dimensions, dates, and flags (128,975 rows × 37 columns).
5. [`Data/Processed/amazon_sales_analytics.csv`](file:///c:/Users/kbhan/OneDrive/Desktop/Projects/AI-Ecommerce-Analytics-Dashboard/Data/Processed/amazon_sales_analytics.csv): Optimized analytics-ready dataset for SQL, Power BI, and ML modeling (128,975 rows × 36 columns).

---
*End of Phase 2 Cleaning Report. Awaiting user review before starting Phase 3.*
