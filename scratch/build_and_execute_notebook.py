import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbclient import NotebookClient

notebook_path = r'c:\Users\kbhan\OneDrive\Desktop\Projects\AI-Ecommerce-Analytics-Dashboard\Analysis\03_eda.ipynb'
work_dir = r'c:\Users\kbhan\OneDrive\Desktop\Projects\AI-Ecommerce-Analytics-Dashboard\Analysis'

nb = new_notebook()

# Section 1: Title & Project Overview
nb.cells.append(new_markdown_cell(
"""# Phase 3: Exploratory Data Analysis (EDA) & Business Intelligence

**Project:** AI-Powered E-Commerce Analytics Dashboard  
**Dataset:** `Data/Processed/amazon_sales_analytics.csv` (128,975 rows × 36 columns)  
**Author:** Antigravity AI  
**Date:** September 5, 2026  

---

### Project Overview & Objectives
This notebook implements the complete **Phase 3 Exploratory Data Analysis (EDA)** workflow for the Amazon Sales Analytics dataset. The goal is to uncover core business patterns, validate data quality, analyze customer purchasing behavior, evaluate revenue realization across categories and geographies, and extract executive KPIs for future SQL modeling, Power BI dashboard development, and Machine Learning pipelines.

---

### Notebook Structure:
1. **Title & Project Overview**
2. **Import Libraries**
3. **Load Analytics Dataset**
4. **Dataset Overview**
5. **Data Quality Validation**
6. **Univariate Analysis** (Status, Category, Fulfillment, Promotions, Geography, Quantity, Revenue)
7. **Bivariate Business Analysis** (Category vs Revenue, State vs Revenue, Status vs Revenue, Promotion vs Revenue, Fulfillment vs Revenue, Category vs Cancellation)
8. **Monthly Performance**
9. **Daily Performance**
10. **Business KPIs**
11. **Key Business Insights**
12. **Final Validation**
"""
))

# Section 2: Import Libraries
nb.cells.append(new_markdown_cell(
"""## 2. Import Libraries

We import standard data science and visualization libraries: `pandas`, `numpy`, and `matplotlib.pyplot`. Matplotlib aesthetics are configured for clear, publication-quality visualizations.
"""
))
nb.cells.append(new_code_cell(
"""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure matplotlib aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['figure.autolayout'] = True

# Setup paths
data_path = os.path.join('..', 'Data', 'Processed', 'amazon_sales_analytics.csv')
output_dir = os.path.join('EDA_Outputs')
os.makedirs(output_dir, exist_ok=True)

print("Environment configured successfully!")
"""
))

# Section 3: Load Analytics Dataset
nb.cells.append(new_markdown_cell(
"""## 3. Load Analytics Dataset

We load the clean, preprocessed dataset `Data/Processed/amazon_sales_analytics.csv` created during Phase 2. The `Date` column is converted to `datetime64[ns]`.
"""
))
nb.cells.append(new_code_cell(
"""# Load dataset
df = pd.read_csv(data_path, low_memory=False)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

print(f"Dataset successfully loaded from: {data_path}")
print(f"Dataset Dimensions: {df.shape[0]:,} rows × {df.shape[1]} columns")
"""
))

# Section 4: Dataset Overview
nb.cells.append(new_markdown_cell(
"""## 4. Dataset Overview

We inspect the first 5 rows, last 5 rows, column names, and data types across the 36 attributes.
"""
))
nb.cells.append(new_code_cell(
"""# First 5 rows preview
preview_cols = ['Order_ID', 'Date', 'Status', 'Category', 'Size', 'Qty', 'Gross_Amount', 'Realized_Revenue', 'Ship_State', 'Is_Cancelled']
print("--- First 5 Rows ---")
df[preview_cols].head()
"""
))
nb.cells.append(new_code_cell(
"""# Last 5 rows preview
print("--- Last 5 Rows ---")
df[preview_cols].tail()
"""
))
nb.cells.append(new_code_cell(
"""# Column inventory and types summary
schema_df = pd.DataFrame({
    'Column Name': df.columns,
    'Data Type': df.dtypes.astype(str),
    'Non-Null Count': df.notnull().sum().values,
    'Null Count': df.isnull().sum().values
})
print(f"Total Columns: {len(schema_df)}")
schema_df.head(18)
"""
))

# Section 5: Data Quality Validation
nb.cells.append(new_markdown_cell(
"""## 5. Data Quality Validation

We verify missing value counts across all active analytics columns, check for duplicate rows, and validate the Phase 2 financial invariant:
$$\\text{Realized\\_Revenue} \\le \\text{Gross\\_Amount}$$
"""
))
nb.cells.append(new_code_cell(
"""# Missing values & duplicate rows check
active_missing = df.drop(columns=['Recorded_Amount']).isnull().sum().sum()
raw_audit_missing = df['Recorded_Amount'].isnull().sum()
full_duplicates = df.duplicated().sum()
unique_orders = df['Order_ID'].nunique()

print(f"Missing values in active analytics columns: {active_missing}")
print(f"Missing values in raw Recorded_Amount audit column: {raw_audit_missing:,} (Preserved intentionally)")
print(f"Exact Full Duplicate Rows: {full_duplicates}")
print(f"Unique Order IDs:          {unique_orders:,}")

# Invariant check
violations = (df['Realized_Revenue'] > df['Gross_Amount']).sum()
print(f"Invariant Violations (Realized_Revenue <= Gross_Amount): {violations}")
assert violations == 0, "Financial invariant check failed!"
print("Status: Data Quality Validation PASSED (100% Consistent)")
"""
))

# Section 6: Univariate Analysis
nb.cells.append(new_markdown_cell(
"""## 6. Univariate Analysis

We examine the distributions of individual operational, product, geographic, and financial variables:
- **Order Status**
- **Product Category**
- **Fulfillment Channel**
- **Promotions**
- **Geography (Top States & Cities)**
- **Quantity Ordered**
- **Revenue Distribution**
"""
))
nb.cells.append(new_code_cell(
"""# 6.1 Order Status Distribution
status_counts = df['Status'].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(range(len(status_counts)), status_counts.values[::-1], color='#1f77b4')
ax.set_yticks(range(len(status_counts)))
ax.set_yticklabels(status_counts.index[::-1])
ax.set_title('Order Status Distribution (Transaction Counts)')
ax.set_xlabel('Number of Orders / Line Items')
ax.set_ylabel('Order Status')

for bar in bars:
    w = bar.get_width()
    pct = (w / len(df)) * 100
    ax.text(w + 800, bar.get_y() + bar.get_height()/2, f"{int(w):,} ({pct:.1f}%)", va='center', ha='left', fontsize=8)
ax.set_xlim(0, max(status_counts.values) * 1.18)

plt.savefig(os.path.join(output_dir, 'status_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))
nb.cells.append(new_code_cell(
"""# 6.2 Product Category Distribution & Revenue
cat_summary = df.groupby('Category').agg(
    Order_Count=('Order_ID', 'count'),
    Total_Qty=('Qty', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
).sort_values(by='Realized_Revenue', ascending=False)

# Category count chart
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(range(len(cat_summary)), cat_summary['Order_Count'], color='#2ca02c')
ax.set_title('Product Category Distribution (Order Line Counts)')
ax.set_ylabel('Number of Transactions')
ax.set_xticks(range(len(cat_summary)))
ax.set_xticklabels(cat_summary.index, rotation=30, ha='right')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1000, f"{int(yval):,}", ha='center', va='bottom', fontsize=8)
ax.set_ylim(0, max(cat_summary['Order_Count']) * 1.12)
plt.savefig(os.path.join(output_dir, 'category_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()

# Category revenue chart
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(range(len(cat_summary)), cat_summary['Realized_Revenue'] / 1e6, color='#ff7f0e')
ax.set_title('Realized Revenue by Product Category (INR Millions)')
ax.set_ylabel('Realized Revenue (₹ Millions)')
ax.set_xticks(range(len(cat_summary)))
ax.set_xticklabels(cat_summary.index, rotation=30, ha='right')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"₹{yval:.2f}M", ha='center', va='bottom', fontsize=8)
ax.set_ylim(0, max(cat_summary['Realized_Revenue'] / 1e6) * 1.12)
plt.savefig(os.path.join(output_dir, 'category_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))
nb.cells.append(new_code_cell(
"""# 6.3 Fulfillment Channel Distribution & Revenue
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

fulfilment_counts = df['Fulfilment'].value_counts()
axes[0].pie(fulfilment_counts, labels=fulfilment_counts.index, autopct='%1.1f%%', 
            colors=['#4a7bb0', '#88c27a'], startangle=140, explode=(0.04, 0))
axes[0].set_title('Fulfillment Channel (Amazon FBA vs Merchant)')

fulfil_rev = df.groupby('Fulfilment')['Realized_Revenue'].sum() / 1e6
bars = axes[1].bar(range(len(fulfil_rev)), fulfil_rev.values, color=['#4a7bb0', '#88c27a'], width=0.5)
axes[1].set_title('Realized Revenue by Fulfillment Channel (₹ Millions)')
axes[1].set_ylabel('Realized Revenue (₹ Millions)')
axes[1].set_xticks(range(len(fulfil_rev)))
axes[1].set_xticklabels(fulfil_rev.index)
for bar in bars:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval + 0.8, f"₹{yval:.2f}M", ha='center', va='bottom')
axes[1].set_ylim(0, max(fulfil_rev.values) * 1.15)

plt.savefig(os.path.join(output_dir, 'fulfillment_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))
nb.cells.append(new_code_cell(
"""# 6.4 Promotions Distribution & Revenue Comparison
fig, ax = plt.subplots(figsize=(6, 4))
promo_counts = df['Has_Promotion'].value_counts()
ax.pie(promo_counts, labels=['Promoted (True)', 'No Promotion (False)'], autopct='%1.1f%%',
       colors=['#e377c2', '#bcbd22'], startangle=90, explode=(0.04, 0))
ax.set_title('Proportion of Transactions with Promotions Applied')
plt.savefig(os.path.join(output_dir, 'promotion_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()

# Revenue Comparison Chart
promo_fin = df.groupby('Has_Promotion').agg(
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
) / 1e6

x = np.arange(len(promo_fin.index))
width = 0.35
fig, ax = plt.subplots(figsize=(8, 4.5))
bars1 = ax.bar(x - width/2, promo_fin['Gross_Amount'], width, label='Gross Amount', color='#9467bd')
bars2 = ax.bar(x + width/2, promo_fin['Realized_Revenue'], width, label='Realized Revenue', color='#17becf')

ax.set_title('Gross Amount vs Realized Revenue by Promotion Status (₹ Millions)')
ax.set_ylabel('Amount (₹ Millions)')
ax.set_xticks(x)
ax.set_xticklabels(['No Promotion (False)', 'Promoted (True)'])
ax.legend()

for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.6, f"₹{yval:.1f}M", ha='center', va='bottom', fontsize=8)
for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.6, f"₹{yval:.1f}M", ha='center', va='bottom', fontsize=8)
    
ax.set_ylim(0, max(promo_fin['Gross_Amount']) * 1.15)
plt.savefig(os.path.join(output_dir, 'promotion_revenue_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))
nb.cells.append(new_code_cell(
"""# 6.5 Geographic Analysis (Top States & Cities)
# Top 15 States by Orders
top_states_ord = df['Ship_State'].value_counts().head(15)
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(range(len(top_states_ord)), top_states_ord.values[::-1], color='#3470a3')
ax.set_yticks(range(len(top_states_ord)))
ax.set_yticklabels(top_states_ord.index[::-1])
ax.set_title('Top 15 States by Order Volume (Transaction Counts)')
ax.set_xlabel('Order Count')
for bar in bars:
    w = bar.get_width()
    ax.text(w + 300, bar.get_y() + bar.get_height()/2, f"{int(w):,}", va='center', ha='left', fontsize=8)
ax.set_xlim(0, max(top_states_ord.values) * 1.14)
plt.savefig(os.path.join(output_dir, 'top_states_orders.png'), dpi=300, bbox_inches='tight')
plt.show()

# Top 15 States by Realized Revenue
state_rev = df.groupby('Ship_State')['Realized_Revenue'].sum().sort_values(ascending=False).head(15) / 1e6
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(range(len(state_rev)), state_rev.values[::-1], color='#d95f02')
ax.set_yticks(range(len(state_rev)))
ax.set_yticklabels(state_rev.index[::-1])
ax.set_title('Top 15 States by Realized Revenue (₹ Millions)')
ax.set_xlabel('Realized Revenue (₹ Millions)')
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.15, bar.get_y() + bar.get_height()/2, f"₹{w:.2f}M", va='center', ha='left', fontsize=8)
ax.set_xlim(0, max(state_rev.values) * 1.15)
plt.savefig(os.path.join(output_dir, 'top_states_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()

# Top 15 Cities by Realized Revenue
city_rev = df[df['Ship_City'] != 'Unknown/Not Provided'].groupby('Ship_City')['Realized_Revenue'].sum().sort_values(ascending=False).head(15) / 1e6
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(range(len(city_rev)), city_rev.values[::-1], color='#7570b3')
ax.set_yticks(range(len(city_rev)))
ax.set_yticklabels(city_rev.index[::-1])
ax.set_title('Top 15 Cities by Realized Revenue (₹ Millions)')
ax.set_xlabel('Realized Revenue (₹ Millions)')
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.08, bar.get_y() + bar.get_height()/2, f"₹{w:.2f}M", va='center', ha='left', fontsize=8)
ax.set_xlim(0, max(city_rev.values) * 1.15)
plt.savefig(os.path.join(output_dir, 'top_cities_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))
nb.cells.append(new_code_cell(
"""# 6.6 Quantity & Revenue Distributions
qty_counts = df['Qty'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(range(len(qty_counts)), qty_counts.values, color='#1b9e77')
ax.set_title('Distribution of Order Quantities (Logarithmic Scale)')
ax.set_xlabel('Quantity Ordered')
ax.set_ylabel('Transaction Count (Log Scale)')
ax.set_yscale('log')
ax.set_xticks(range(len(qty_counts)))
ax.set_xticklabels(qty_counts.index.astype(str))

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval * 1.15, f"{int(yval):,}", ha='center', va='bottom', fontsize=8)
plt.savefig(os.path.join(output_dir, 'quantity_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()

# Revenue Distribution Histograms & Boxplots
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
realized_positive = df[df['Realized_Revenue'] > 0]['Realized_Revenue']
axes[0].hist(realized_positive, bins=40, color='#386cb0', edgecolor='white')
axes[0].set_title('Realized Revenue Distribution (Non-Zero Orders)')
axes[0].set_xlabel('Realized Amount (₹)')
axes[0].set_ylabel('Frequency')

axes[1].boxplot([df['Gross_Amount'], realized_positive], tick_labels=['All Gross Amount', 'Non-Zero Realized Revenue'])
axes[1].set_title('Gross vs Realized Revenue Boxplot Distribution')
axes[1].set_ylabel('Amount (₹)')

plt.savefig(os.path.join(output_dir, 'revenue_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()
"""
))

# Section 7: Bivariate Business Analysis
nb.cells.append(new_markdown_cell(
"""## 7. Bivariate Business Analysis

We analyze relationships between cross-functional business attributes:
1. **Category vs Revenue & Realization Rate**
2. **State vs Revenue & Cancellation Rate**
3. **Status vs Revenue Comparison**
4. **Promotion vs Realized Revenue**
5. **Fulfillment vs Realization & Cancellation Rates**
6. **Category vs Cancellation Rate & Lost Value**
"""
))
nb.cells.append(new_code_cell(
"""# 7.1 Category vs Revenue & Realization Rate
cat_df = df.groupby('Category').agg(
    Transactions=('Order_ID', 'count'),
    Total_Quantity=('Qty', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
)
cat_df['Realization_Rate_Pct'] = (cat_df['Realized_Revenue'] / cat_df['Gross_Amount'] * 100).round(2)
cat_df = cat_df.sort_values(by='Realized_Revenue', ascending=False)
cat_df.to_csv(os.path.join(output_dir, 'category_performance.csv'))

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(range(len(cat_df)), cat_df['Realization_Rate_Pct'], color='#41b6c4')
ax.set_title('Revenue Realization Rate by Product Category (%)')
ax.set_ylabel('Realization Rate (%)')
ax.set_xticks(range(len(cat_df)))
ax.set_xticklabels(cat_df.index, rotation=30, ha='right')
ax.set_ylim(0, 105)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=8)
plt.savefig(os.path.join(output_dir, 'category_revenue_realization.png'), dpi=300, bbox_inches='tight')
plt.show()

cat_df
"""
))
nb.cells.append(new_code_cell(
"""# 7.2 State vs Revenue & Cancellation Rate
state_df = df.groupby('Ship_State').agg(
    Orders=('Order_ID', 'count'),
    Quantity=('Qty', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum'),
    Cancelled_Orders=('Is_Cancelled', 'sum')
)
state_df['Cancellation_Rate_Pct'] = (state_df['Cancelled_Orders'] / state_df['Orders'] * 100).round(2)
state_df['Realization_Rate_Pct'] = (state_df['Realized_Revenue'] / state_df['Gross_Amount'] * 100).round(2)
state_df = state_df.sort_values(by='Realized_Revenue', ascending=False)
state_df.to_csv(os.path.join(output_dir, 'state_performance.csv'))

top10_state = state_df.head(10)
fig, ax1 = plt.subplots(figsize=(11, 4.5))

ax1.bar(range(len(top10_state)), top10_state['Realized_Revenue'] / 1e6, color='#2b8cbe', label='Realized Revenue (₹M)')
ax1.set_ylabel('Realized Revenue (₹ Millions)', color='#2b8cbe')
ax1.set_xticks(range(len(top10_state)))
ax1.set_xticklabels(top10_state.index, rotation=30, ha='right')
ax1.set_title('Top 10 States: Realized Revenue and Cancellation Rate')

ax2 = ax1.twinx()
ax2.plot(range(len(top10_state)), top10_state['Cancellation_Rate_Pct'], color='#de2d26', marker='o', lw=2, label='Cancellation Rate (%)')
ax2.set_ylabel('Cancellation Rate (%)', color='#de2d26')
ax2.set_ylim(0, 25)

plt.savefig(os.path.join(output_dir, 'state_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()

top10_state
"""
))
nb.cells.append(new_code_cell(
"""# 7.3 Status vs Revenue
status_df = df.groupby('Status').agg(
    Order_Count=('Order_ID', 'count'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
).sort_values(by='Gross_Amount', ascending=False)
status_df['Avg_Gross_Line_Value'] = (status_df['Gross_Amount'] / status_df['Order_Count']).round(2)

fig, ax = plt.subplots(figsize=(11, 5))
top7_status = status_df.head(7)
x = np.arange(len(top7_status))
width = 0.35

ax.bar(x - width/2, top7_status['Gross_Amount'] / 1e6, width, label='Gross Amount', color='#74a9cf')
ax.bar(x + width/2, top7_status['Realized_Revenue'] / 1e6, width, label='Realized Revenue', color='#02818a')

ax.set_title('Top 7 Order Statuses: Gross Amount vs Realized Revenue (₹ Millions)')
ax.set_ylabel('Amount (₹ Millions)')
ax.set_xticks(x)
ax.set_xticklabels(top7_status.index, rotation=30, ha='right')
ax.legend()

plt.savefig(os.path.join(output_dir, 'status_revenue_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()

status_df.head(7)
"""
))
nb.cells.append(new_code_cell(
"""# 7.4 Promotion vs Revenue Performance
promo_df = df.groupby('Has_Promotion').agg(
    Transactions=('Order_ID', 'count'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
)
promo_df['Avg_Realized_Revenue'] = (promo_df['Realized_Revenue'] / promo_df['Transactions']).round(2)
promo_df['Realization_Rate_Pct'] = (promo_df['Realized_Revenue'] / promo_df['Gross_Amount'] * 100).round(2)
promo_df.to_csv(os.path.join(output_dir, 'promotion_performance.csv'))

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(['No Promotion (False)', 'Promoted (True)'], promo_df['Avg_Realized_Revenue'], 
              color=['#fd8d3c', '#807dba'], width=0.45)
ax.set_title('Observed Average Realized Revenue per Line Item (₹)')
ax.set_ylabel('Average Realized Revenue (₹)')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f"₹{yval:.2f}", ha='center', va='bottom')
ax.set_ylim(0, max(promo_df['Avg_Realized_Revenue']) * 1.15)
plt.savefig(os.path.join(output_dir, 'promotion_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()

promo_df
"""
))
nb.cells.append(new_code_cell(
"""# 7.5 Fulfillment Channel Performance
ful_df = df.groupby(['Fulfilment', 'Fulfilled_By']).agg(
    Order_Count=('Order_ID', 'count'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum'),
    Cancelled_Orders=('Is_Cancelled', 'sum')
)
ful_df['Cancellation_Rate_Pct'] = (ful_df['Cancelled_Orders'] / ful_df['Order_Count'] * 100).round(2)
ful_df['Realization_Rate_Pct'] = (ful_df['Realized_Revenue'] / ful_df['Gross_Amount'] * 100).round(2)
ful_df.to_csv(os.path.join(output_dir, 'fulfillment_performance.csv'))

ful_summary = df.groupby('Fulfilment').agg(
    Cancellation_Rate=('Is_Cancelled', lambda x: (x.sum()/len(x))*100),
    Realization_Rate=('Realized_Revenue', lambda x: (x.sum()/df.loc[x.index, 'Gross_Amount'].sum())*100)
)

fig, ax1 = plt.subplots(figsize=(7, 4.5))
x = np.arange(len(ful_summary.index))
width = 0.35
ax1.bar(x - width/2, ful_summary['Realization_Rate'], width, label='Realization Rate (%)', color='#41ab5d')
ax1.bar(x + width/2, ful_summary['Cancellation_Rate'], width, label='Cancellation Rate (%)', color='#ef3b2c')

ax1.set_title('Fulfillment Channel: Realization vs Cancellation Rates')
ax1.set_ylabel('Rate (%)')
ax1.set_xticks(x)
ax1.set_xticklabels(ful_summary.index)
ax1.legend()
ax1.set_ylim(0, 105)

plt.savefig(os.path.join(output_dir, 'fulfillment_revenue.png'), dpi=300, bbox_inches='tight')
plt.show()

ful_df
"""
))
nb.cells.append(new_code_cell(
"""# 7.6 Category vs Cancellation Rate & Lost Value
cat_canc = df.groupby('Category').agg(
    Total_Transactions=('Order_ID', 'count'),
    Cancelled_Transactions=('Is_Cancelled', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum')
)
cat_canc['Cancellation_Rate_Pct'] = (cat_canc['Cancelled_Transactions'] / cat_canc['Total_Transactions'] * 100).round(2)
cat_canc['Unrealized_Lost_Value'] = (cat_canc['Gross_Amount'] - cat_canc['Realized_Revenue']).round(2)
cat_canc = cat_canc.sort_values(by='Cancellation_Rate_Pct', ascending=False)
cat_canc.to_csv(os.path.join(output_dir, 'category_cancellation.csv'))

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(range(len(cat_canc)), cat_canc['Cancellation_Rate_Pct'], color='#fb6a4a')
ax.set_title('Order Cancellation Rate by Product Category (%)')
ax.set_ylabel('Cancellation Rate (%)')
ax.set_xticks(range(len(cat_canc)))
ax.set_xticklabels(cat_canc.index, rotation=30, ha='right')
ax.set_ylim(0, max(cat_canc['Cancellation_Rate_Pct']) * 1.2)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontsize=8)
    
plt.savefig(os.path.join(output_dir, 'category_cancellation_rate.png'), dpi=300, bbox_inches='tight')
plt.show()

cat_canc
"""
))

# Section 8: Monthly Performance
nb.cells.append(new_markdown_cell(
"""## 8. Monthly Performance

We analyze aggregated monthly trends in transaction volume, gross listed amounts, and net realized revenue across Q2 2022.
"""
))
nb.cells.append(new_code_cell(
"""monthly = df.groupby(['Year', 'Month', 'Month_Name']).agg(
    Orders=('Order_ID', 'count'),
    Quantity=('Qty', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum'),
    Cancelled_Orders=('Is_Cancelled', 'sum')
).reset_index()
monthly['Cancellation_Rate_Pct'] = (monthly['Cancelled_Orders'] / monthly['Orders'] * 100).round(2)
monthly = monthly.sort_values(by=['Year', 'Month'])
monthly.to_csv(os.path.join(output_dir, 'monthly_sales.csv'), index=False)

# Monthly Volume Trend
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly['Month_Name'], monthly['Orders'], marker='o', color='#1f78b4', lw=2.5)
ax.set_title('Monthly Order Volume Trend (Q2 2022)')
ax.set_ylabel('Number of Order Lines')
for x_val, y_val in zip(monthly['Month_Name'], monthly['Orders']):
    ax.text(x_val, y_val + 700, f"{int(y_val):,}", ha='center', va='bottom', fontsize=9)
ax.set_ylim(0, max(monthly['Orders']) * 1.15)
plt.savefig(os.path.join(output_dir, 'monthly_sales_trend.png'), dpi=300, bbox_inches='tight')
plt.show()

# Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly['Month_Name'], monthly['Gross_Amount'] / 1e6, marker='s', color='#33a02c', lw=2, label='Gross Listed (₹M)')
ax.plot(monthly['Month_Name'], monthly['Realized_Revenue'] / 1e6, marker='o', color='#e31a1c', lw=2.5, label='Realized Net Revenue (₹M)')
ax.set_title('Monthly Revenue Trend: Gross Listed vs Realized Net (₹ Millions)')
ax.set_ylabel('Revenue (₹ Millions)')
ax.legend()
for x_val, y_val in zip(monthly['Month_Name'], monthly['Realized_Revenue'] / 1e6):
    ax.text(x_val, y_val + 0.6, f"₹{y_val:.2f}M", ha='center', va='bottom', fontsize=9)
ax.set_ylim(0, max(monthly['Gross_Amount'] / 1e6) * 1.15)
plt.savefig(os.path.join(output_dir, 'monthly_revenue_trend.png'), dpi=300, bbox_inches='tight')
plt.show()

monthly
"""
))

# Section 9: Daily Performance
nb.cells.append(new_markdown_cell(
"""## 9. Daily Performance

We track daily revenue trends and compute a 7-day moving average to smooth weekday/weekend seasonality.
"""
))
nb.cells.append(new_code_cell(
"""daily = df.groupby(df['Date'].dt.date).agg(
    Orders=('Order_ID', 'count'),
    Quantity=('Qty', 'sum'),
    Gross_Amount=('Gross_Amount', 'sum'),
    Realized_Revenue=('Realized_Revenue', 'sum')
).reset_index().rename(columns={'Date': 'Order_Date'})
daily.to_csv(os.path.join(output_dir, 'daily_sales.csv'), index=False)

fig, ax = plt.subplots(figsize=(13, 4.5))
daily_dates = pd.to_datetime(daily['Order_Date'])
ax.plot(daily_dates, daily['Realized_Revenue'] / 1e3, color='#08519c', lw=1.5, label='Daily Realized Revenue (₹ Thousands)')

# 7-day moving average
rolling_7 = (daily['Realized_Revenue'] / 1e3).rolling(7).mean()
ax.plot(daily_dates, rolling_7, color='#e6550d', lw=2.2, label='7-Day Moving Average')

ax.set_title('Daily Realized Revenue Trend with 7-Day Moving Average (Q2 2022)')
ax.set_xlabel('Date')
ax.set_ylabel('Realized Revenue (₹ Thousands)')
ax.legend()
plt.savefig(os.path.join(output_dir, 'daily_revenue_trend.png'), dpi=300, bbox_inches='tight')
plt.show()

daily.head()
"""
))

# Section 10: Business KPIs
nb.cells.append(new_markdown_cell(
"""## 10. Business KPIs

We calculate the 12 core executive KPIs required for strategic reporting and executive dashboard cards.
"""
))
nb.cells.append(new_code_cell(
"""total_orders = df['Order_ID'].nunique()
total_lines = len(df)
total_gross = df['Gross_Amount'].sum()
total_realized = df['Realized_Revenue'].sum()
unrealized = total_gross - total_realized

kpis = [
    {'KPI Metric': 'Total Unique Orders', 'Value': f"{total_orders:,}", 'Unit / Type': 'Orders'},
    {'KPI Metric': 'Total Order Line Items', 'Value': f"{total_lines:,}", 'Unit / Type': 'Line Items'},
    {'KPI Metric': 'Total Units Ordered', 'Value': f"{df['Qty'].sum():,}", 'Unit / Type': 'Pieces'},
    {'KPI Metric': 'Total Gross Listed Amount', 'Value': f"₹{total_gross:,.2f}", 'Unit / Type': 'INR'},
    {'KPI Metric': 'Total Realized Net Revenue', 'Value': f"₹{total_realized:,.2f}", 'Unit / Type': 'INR'},
    {'KPI Metric': 'Total Unrealized / Lost Value', 'Value': f"₹{unrealized:,.2f}", 'Unit / Type': 'INR'},
    {'KPI Metric': 'Overall Realization Rate', 'Value': f"{(total_realized/total_gross)*100:.2f}%", 'Unit / Type': 'Percentage'},
    {'KPI Metric': 'Overall Cancellation Rate', 'Value': f"{(df['Is_Cancelled'].sum()/total_lines)*100:.2f}%", 'Unit / Type': 'Percentage'},
    {'KPI Metric': 'Overall Return Rate', 'Value': f"{(df['Is_Returned'].sum()/total_lines)*100:.2f}%", 'Unit / Type': 'Percentage'},
    {'KPI Metric': 'Promotion Usage Rate', 'Value': f"{(df['Has_Promotion'].sum()/total_lines)*100:.2f}%", 'Unit / Type': 'Percentage'},
    {'KPI Metric': 'Average Gross Line Value', 'Value': f"₹{df['Gross_Amount'].mean():.2f}", 'Unit / Type': 'INR'},
    {'KPI Metric': 'Average Realized Line Value', 'Value': f"₹{df['Realized_Revenue'].mean():.2f}", 'Unit / Type': 'INR'}
]

kpi_df = pd.DataFrame(kpis)
kpi_df
"""
))

# Section 11: Key Business Insights
nb.cells.append(new_markdown_cell(
"""## 11. Key Business Insights

Summary of the top strategic takeaways discovered through EDA:
1. **Hero Category Concentration:** `Set` (₹35.53M / 50.55%) and `Kurta` (₹18.89M / 26.87%) drive **77.42% of total realized sales**.
2. **Growth Vector:** `Western Dress` (₹10.05M / 14.30%) is the 3rd largest category with premium unit economics.
3. **Geographic Engines:** **Maharashtra** (₹11.96M) and **Karnataka** (₹9.52M) lead state sales. Top metro hubs are **Bengaluru** (₹6.15M), **Hyderabad** (₹4.46M), and **Mumbai** (₹3.17M).
4. **Uniform Realization:** Realization rates across core apparel range between **88.7% and 89.7%**.
5. **Pre-dispatch Cancellations:** Cancellation accounts for **₹6.92M in lost value (14.21%)**, making it the primary operational efficiency target.
6. **Low Returns:** Post-dispatch customer return rate is remarkably healthy at **1.64% (₹1.38M)**.
7. **Fulfillment Dominance:** **Amazon FBA** commands **69.55% volume**, with lower cancellation rates (12.87%) compared to Merchant Easy Ship (17.27%).
8. **Promotion Penetration:** 61.89% of transactions used promotional discount coupons, averaging ₹549.91 per line.
9. **Quarterly Trajectory:** Sales peaked in **April 2022** (₹26.54M) and contracted toward **June 2022** (₹20.73M).
10. **B2B Channel:** Wholesale B2B GST accounts for **0.68% volume (₹599.7K)** with larger basket sizes.
"""
))

# Section 12: Final Validation
nb.cells.append(new_markdown_cell(
"""## 12. Final Validation

We verify dataset shape immutability, zero invariant violations, and pipeline repeatability.
"""
))
nb.cells.append(new_code_cell(
"""# Final automated validation assertions
assert df.shape == (128975, 36), f"Dataset shape modified! Current: {df.shape}"
assert (df['Realized_Revenue'] <= df['Gross_Amount']).all(), "Financial invariant violated!"
assert os.path.exists(os.path.join(output_dir, 'category_performance.csv')), "Output CSV missing!"
assert os.path.exists(os.path.join(output_dir, 'category_revenue.png')), "Output Chart missing!"

print("=" * 60)
print("ALL VALIDATION ASSERTIONS PASSED WITH ZERO ERRORS!")
print("=" * 60)
"""
))

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Constructed {len(nb.cells)} cells in notebook: {notebook_path}")

# Execute notebook using NotebookClient to verify all cells and persist outputs
print("Executing notebook to verify zero errors...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb_to_run = nbformat.read(f, as_version=4)

client = NotebookClient(nb_to_run, timeout=600, kernel_name='python3', resources={'metadata': {'path': work_dir}})
client.execute()

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb_to_run, f)

print("Notebook executed and saved successfully with all cell outputs!")
