"""
AI-Ecommerce-Analytics-Dashboard: Phase 2 Data Cleaning & Preprocessing Pipeline
Author: AI Assistant
Date: 2026-09-05
"""

import os
import re
import pandas as pd
import numpy as np

def clean_amazon_sales_data(raw_data_path=None, output_dir=None):
    # Determine default paths if not provided
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if raw_data_path is None:
        raw_data_path = os.path.join(base_dir, 'Data', 'Raw Data', 'amazon_sales.csv.csv')
    if output_dir is None:
        output_dir = os.path.join(base_dir, 'Data', 'Processed')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("PHASE 2: DATA CLEANING & PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # 1. LOAD DATA
    print(f"\n[1/8] Loading raw data from: {raw_data_path}")
    df_raw = pd.read_csv(raw_data_path, low_memory=False)
    initial_rows, initial_cols = df_raw.shape
    print(f"  -> Raw dataset loaded: {initial_rows:,} rows, {initial_cols} columns")
    
    df = df_raw.copy()
    
    # 2. COLUMN CLEANING & DROPPING REDUNDANT COLUMNS
    print("\n[2/8] Standardizing column names and removing redundant artifact columns...")
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]
    
    # Drop redundant export artifact columns
    cols_to_drop = ['index', 'Unnamed: 22']
    dropped = [c for c in cols_to_drop if c in df.columns]
    df.drop(columns=dropped, inplace=True)
    print(f"  -> Dropped columns: {dropped}")
    
    # Rename columns to standard PascalCase format
    column_renaming = {
        'Order ID': 'Order_ID',
        'Sales Channel': 'Sales_Channel',
        'ship-service-level': 'Ship_Service_Level',
        'Courier Status': 'Courier_Status',
        'ship-city': 'Ship_City',
        'ship-state': 'Ship_State',
        'ship-postal-code': 'Ship_Postal_Code',
        'ship-country': 'Ship_Country',
        'promotion-ids': 'Promotion_IDs',
        'fulfilled-by': 'Fulfilled_By',
        'Amount': 'Recorded_Amount',
        'currency': 'Currency'
    }
    df.rename(columns=column_renaming, inplace=True)
    print(f"  -> Standardized column headers: {list(df.columns)}")
    
    # 3. DATE CLEANING & DERIVED TEMPORAL COLUMNS
    print("\n[3/8] Parsing dates and engineering temporal features...")
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')
    
    # Derived temporal columns
    df['Year'] = df['Date'].dt.year.astype('int32')
    df['Month'] = df['Date'].dt.month.astype('int32')
    df['Month_Name'] = df['Date'].dt.month_name()
    df['Week'] = df['Date'].dt.isocalendar().week.astype('int32')
    df['Day'] = df['Date'].dt.day.astype('int32')
    df['Day_Name'] = df['Date'].dt.day_name()
    print(f"  -> Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    print("  -> Created derived date columns: Year, Month, Month_Name, Week, Day, Day_Name")
    
    # 4. TEXT STANDARDIZATION & CATEGORICAL FIELDS
    print("\n[4/8] Standardizing categorical fields and text values...")
    # Category: standardize casing (e.g. 'kurta' -> 'Kurta')
    df['Category'] = df['Category'].astype(str).str.strip().str.title()
    
    # Size: strip & uppercase
    df['Size'] = df['Size'].astype(str).str.strip().str.upper()
    
    # Status, Fulfilment, Sales_Channel, Ship_Service_Level
    df['Status'] = df['Status'].astype(str).str.strip()
    df['Fulfilment'] = df['Fulfilment'].astype(str).str.strip()
    df['Sales_Channel'] = df['Sales_Channel'].astype(str).str.strip()
    df['Ship_Service_Level'] = df['Ship_Service_Level'].astype(str).str.strip()
    
    # Ship_City: clean whitespace & title case
    df['Ship_City'] = df['Ship_City'].fillna('Unknown/Not Provided').astype(str).str.strip().str.title()
    
    # Ship_Country: clean whitespace & uppercase
    df['Ship_Country'] = df['Ship_Country'].fillna('Unknown/Not Provided').astype(str).str.strip().str.upper()
    
    # 5. STATE STANDARDIZATION
    print("\n[5/8] Standardizing ship-state names and handling regional variations...")
    STATE_MAPPING = {
        'MAHARASHTRA': 'Maharashtra',
        'KARNATAKA': 'Karnataka',
        'TAMIL NADU': 'Tamil Nadu',
        'TELANGANA': 'Telangana',
        'UTTAR PRADESH': 'Uttar Pradesh',
        'DELHI': 'Delhi',
        'Delhi': 'Delhi',
        'delhi': 'Delhi',
        'New Delhi': 'Delhi',
        'KERALA': 'Kerala',
        'WEST BENGAL': 'West Bengal',
        'ANDHRA PRADESH': 'Andhra Pradesh',
        'Gujarat': 'Gujarat',
        'HARYANA': 'Haryana',
        'RAJASTHAN': 'Rajasthan',
        'Rajasthan': 'Rajasthan',
        'rajasthan': 'Rajasthan',
        'Rajshthan': 'Rajasthan',
        'rajsthan': 'Rajasthan',
        'Rajsthan': 'Rajasthan',
        'RJ': 'Rajasthan',
        'MADHYA PRADESH': 'Madhya Pradesh',
        'ODISHA': 'Odisha',
        'Odisha': 'Odisha',
        'Orissa': 'Odisha',
        'orissa': 'Odisha',
        'BIHAR': 'Bihar',
        'Bihar': 'Bihar',
        'bihar': 'Bihar',
        'PUNJAB': 'Punjab',
        'Punjab': 'Punjab',
        'punjab': 'Punjab',
        'Punjab/Mohali/Zirakpur': 'Punjab',
        'PB': 'Punjab',
        'ASSAM': 'Assam',
        'UTTARAKHAND': 'Uttarakhand',
        'JHARKHAND': 'Jharkhand',
        'GOA': 'Goa',
        'Goa': 'Goa',
        'goa': 'Goa',
        'CHHATTISGARH': 'Chhattisgarh',
        'HIMACHAL PRADESH': 'Himachal Pradesh',
        'JAMMU & KASHMIR': 'Jammu and Kashmir',
        'PUDUCHERRY': 'Puducherry',
        'Puducherry': 'Puducherry',
        'Pondicherry': 'Puducherry',
        'CHANDIGARH': 'Chandigarh',
        'Chandigarh': 'Chandigarh',
        'MANIPUR': 'Manipur',
        'Manipur': 'Manipur',
        'ANDAMAN & NICOBAR ': 'Andaman and Nicobar Islands',
        'MEGHALAYA': 'Meghalaya',
        'Meghalaya': 'Meghalaya',
        'SIKKIM': 'Sikkim',
        'Sikkim': 'Sikkim',
        'NAGALAND': 'Nagaland',
        'Nagaland': 'Nagaland',
        'NL': 'Nagaland',
        'TRIPURA': 'Tripura',
        'ARUNACHAL PRADESH': 'Arunachal Pradesh',
        'Arunachal Pradesh': 'Arunachal Pradesh',
        'Arunachal pradesh': 'Arunachal Pradesh',
        'AR': 'Arunachal Pradesh',
        'MIZORAM': 'Mizoram',
        'Mizoram': 'Mizoram',
        'DADRA AND NAGAR': 'Dadra and Nagar Haveli and Daman and Diu',
        'LADAKH': 'Ladakh',
        'LAKSHADWEEP': 'Lakshadweep',
        'APO': 'Unknown/Other'
    }
    df['Ship_State'] = df['Ship_State'].map(STATE_MAPPING).fillna('Unknown/Not Provided')
    print(f"  -> Mapped 69 raw state variations to {df['Ship_State'].nunique()} standardized states/territories.")
    
    # 6. POSTAL CODE STANDARDIZATION & VALIDATION
    print("\n[6/8] Formatting postal codes and validating 6-digit Indian PIN codes...")
    def format_pin(val):
        if pd.isnull(val):
            return 'UNKNOWN'
        try:
            val_int = int(float(val))
            return str(val_int).zfill(6)
        except:
            return str(val).strip()
            
    df['Ship_Postal_Code'] = df['Ship_Postal_Code'].apply(format_pin)
    pin_regex = re.compile(r'^[1-9][0-9]{5}$')
    df['Is_Valid_PIN'] = df['Ship_Postal_Code'].apply(lambda p: bool(pin_regex.match(p)))
    print(f"  -> Valid PIN codes: {df['Is_Valid_PIN'].sum():,} ({df['Is_Valid_PIN'].mean()*100:.2f}%)")
    
    # 7. MISSING VALUES, REVENUE METRICS & BUSINESS FLAGS
    print("\n[7/8] Handling missing values, engineering revenue metrics & quality flags...")
    # Fulfilled_By: 'Easy Ship' vs 'Not Applicable' (for Amazon FBA)
    df['Fulfilled_By'] = df['Fulfilled_By'].fillna('Not Applicable')
    
    # Promotion_IDs: 'No Promotion' when null
    df['Promotion_IDs'] = df['Promotion_IDs'].fillna('No Promotion')
    
    # Courier_Status: 'Unassigned' when null
    df['Courier_Status'] = df['Courier_Status'].fillna('Unassigned')
    
    # Currency: 'INR'
    df['Currency'] = df['Currency'].fillna('INR')
    
    # B2B: boolean
    df['B2B'] = df['B2B'].astype(bool)
    
    # Gross / Recorded Amount
    df['Gross_Amount'] = df['Recorded_Amount'].fillna(0.0)
    
    # Business Flags
    df['Is_Cancelled'] = df['Status'] == 'Cancelled'
    df['Is_Delivered'] = df['Status'] == 'Shipped - Delivered to Buyer'
    df['Is_Returned'] = df['Status'].isin([
        'Shipped - Returned to Seller', 
        'Shipped - Returning to Seller', 
        'Shipped - Rejected by Buyer'
    ])
    df['Is_B2B'] = df['B2B']
    df['Has_Promotion'] = df['Promotion_IDs'] != 'No Promotion'
    
    # Realized Revenue Business Rule:
    # Revenue is realized only when:
    # 1. Order is NOT cancelled
    # 2. Order is NOT returned, rejected, lost, or damaged
    # 3. Qty > 0
    # 4. Gross_Amount > 0
    non_realized_statuses = [
        'Cancelled',
        'Shipped - Returned to Seller',
        'Shipped - Returning to Seller',
        'Shipped - Rejected by Buyer',
        'Shipped - Lost in Transit',
        'Shipped - Damaged',
        'Shipping'
    ]
    
    is_realized_condition = (
        (~df['Status'].isin(non_realized_statuses)) & 
        (df['Qty'] > 0) & 
        (df['Gross_Amount'] > 0)
    )
    
    df['Realized_Revenue'] = np.where(is_realized_condition, df['Gross_Amount'], 0.0)
    df['Is_Realized'] = is_realized_condition
    
    print(f"  -> Total Recorded Gross Amount: INR {df['Gross_Amount'].sum():,.2f}")
    print(f"  -> Total Realized Revenue:     INR {df['Realized_Revenue'].sum():,.2f}")
    print(f"  -> Unrealized/Cancelled Value: INR {(df['Gross_Amount'].sum() - df['Realized_Revenue'].sum()):,.2f}")
    
    # 8. SAVE PROCESSED DATASETS
    print("\n[8/8] Saving clean datasets to output directory...")
    clean_csv_path = os.path.join(output_dir, 'amazon_sales_cleaned.csv')
    df.to_csv(clean_csv_path, index=False)
    print(f"  -> Saved full cleaned dataset: {clean_csv_path} ({df.shape[0]:,} rows, {df.shape[1]} cols)")
    
    # Create analytics-ready dataset (compact & structured for BI/ML)
    analytics_columns = [
        'Order_ID', 'Date', 'Year', 'Month', 'Month_Name', 'Week', 'Day', 'Day_Name',
        'Status', 'Courier_Status', 'Fulfilment', 'Fulfilled_By', 'Sales_Channel', 'Ship_Service_Level',
        'Category', 'Size', 'Style', 'SKU', 'ASIN',
        'Qty', 'Currency', 'Recorded_Amount', 'Gross_Amount', 'Realized_Revenue',
        'Ship_City', 'Ship_State', 'Ship_Postal_Code', 'Ship_Country',
        'Promotion_IDs', 'Has_Promotion', 'Is_B2B', 'Is_Cancelled', 'Is_Delivered', 'Is_Returned', 'Is_Realized', 'Is_Valid_PIN'
    ]
    df_analytics = df[analytics_columns]
    analytics_csv_path = os.path.join(output_dir, 'amazon_sales_analytics.csv')
    df_analytics.to_csv(analytics_csv_path, index=False)
    print(f"  -> Saved analytics-ready dataset: {analytics_csv_path} ({df_analytics.shape[0]:,} rows, {df_analytics.shape[1]} cols)")
    
    print("\n" + "=" * 60)
    print("DATA CLEANING PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return df

if __name__ == '__main__':
    clean_amazon_sales_data()
