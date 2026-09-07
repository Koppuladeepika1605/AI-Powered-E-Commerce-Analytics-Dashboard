# Power BI Star Schema - Project Implementation

## 1. Purpose

The Star Schema was created for the Power BI layer of the
AI E-Commerce Analytics Dashboard.

The purpose was to organize the processed Amazon sales data into
separate fact and dimension tables so that the data could be used
efficiently for Power BI analysis and visualization.

---

## 2. Source Data

The Star Schema is generated from:

Data/Processed/amazon_sales_analytics.csv

The Star Schema generator is:

PowerBI/generate_star_schema_tables.py

The script reads the processed analytics dataset and generates
five CSV tables inside:

PowerBI/Model_Tables/

---

## 3. Tables Created

The Power BI model contains:

1. Fact_AmazonSales
2. Dim_Date
3. Dim_Product
4. Dim_Geography
5. Dim_OrderStatus

Therefore, the model consists of:

**1 Fact Table + 4 Dimension Tables**

---

## 4. Fact Table

### Fact_AmazonSales

File:

PowerBI/Model_Tables/Fact_AmazonSales.csv

This is the central sales transaction table.

It contains the actual order-level sales information used for
Power BI analysis.

### Columns Used

- Order_ID
- Date
- SKU
- Qty
- Currency
- Gross_Amount
- Realized_Revenue
- Ship_City
- Ship_State
- Ship_Postal_Code
- Status
- Courier_Status
- Fulfilment
- Has_Promotion
- Is_B2B
- Is_Cancelled
- Is_Delivered
- Is_Returned
- Is_Realized
- Date_Key

The Fact table is mainly used for calculating and analyzing:

- Revenue
- Orders
- Quantity
- Cancellation
- Delivery
- Returns
- Fulfilment
- Order status

---

## 5. Dimension Table - Date

### Dim_Date

File:

PowerBI/Model_Tables/Dim_Date.csv

This table was generated to provide date-related attributes for
time-based analysis.

### Columns

- Date
- Date_Key
- Year
- Quarter
- Month_Number
- Month_Name
- Month_Year
- Week_Number
- Day_Of_Month
- Day_Of_Week
- Day_Name
- Is_Weekend

### Usage in My Dashboard

Dim_Date is used for:

- Date filtering
- Revenue trend analysis
- Monthly analysis
- Time-based reporting

A Date slicer is used in the Power BI dashboard.

---

## 6. Dimension Table - Product

### Dim_Product

File:

PowerBI/Model_Tables/Dim_Product.csv

This table contains product-related information.

### Columns

- SKU
- Style
- Category
- Size
- ASIN

### Usage in My Dashboard

Dim_Product is used for:

- Revenue by Category
- Top Products by Revenue
- Product analysis
- Category analysis

---

## 7. Dimension Table - Geography

### Dim_Geography

File:

PowerBI/Model_Tables/Dim_Geography.csv

This table contains geographical information related to the
customer shipping location.

### Columns

- Geo_ID
- Ship_City
- Ship_State
- Ship_Postal_Code
- Ship_Country
- Is_Valid_PIN

### Usage in My Dashboard

Dim_Geography is used for:

- Revenue by State
- Regional analysis
- Geographical filtering and grouping

---

## 8. Dimension Table - Order Status

### Dim_OrderStatus

File:

PowerBI/Model_Tables/Dim_OrderStatus.csv

This table contains order and fulfilment-related attributes.

### Columns

- Status_ID
- Status
- Courier_Status
- Fulfilment
- Fulfilled_By
- Sales_Channel
- Ship_Service_Level

### Usage in My Dashboard

The order-status information is used for:

- Orders by Status
- Revenue by Fulfilment
- Orders by Courier Status
- Cancellation analysis

Note:

Sales_Channel exists in the generated dimension table, but it is
not used as a visual in my current Power BI dashboard.

---

## 9. Power BI Pages Using the Star Schema

### Page 1 - Executive Overview

The following visuals were created:

1. Total Realized Revenue
2. Total Orders
3. Cancellation Rate %
4. Revenue by Category
5. Realized Revenue Trend
6. Date Slicer

The page provides a high-level overview of e-commerce performance.

---

### Page 2 - Regional & Product Analysis

The following analysis was created:

1. Revenue by State
2. Top Products by Revenue
3. Date Slicer

This page focuses on geographical and product performance.

---

### Page 3 - Operations Analysis

The following visuals were created:

1. Orders by Status
2. Revenue by Fulfilment
3. Orders by Courier Status
4. Cancellation Rate

This page focuses on order and fulfilment operations.

---

## 10. DAX Measures Actually Used

Only the following three DAX measures were created and used
in my current Power BI report.

1. Total Realized Revenue =
SUM(Fact_AmazonSales[Realized_Revenue])
Total Realized Revenue =
SUM(Fact_AmazonSales[Realized_Revenue])


2.Total Orders =
DISTINCTCOUNT(Fact_AmazonSales[Order_ID])


3.Cancellation Rate % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_AmazonSales),
        Fact_AmazonSales[Is_Cancelled] = TRUE
    ),
    COUNTROWS(Fact_AmazonSales),
    0
)