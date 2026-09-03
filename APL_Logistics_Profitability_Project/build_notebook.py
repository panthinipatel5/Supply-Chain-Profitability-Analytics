import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# ---------------------------------------------------------------------------
# TITLE
# ---------------------------------------------------------------------------
md("""# Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

**APL Logistics (KWE Group)** | Unified Mentor Project

---

Leadership question: *Which customers, products, and regions truly generate value for the business?*

This notebook performs the full analytical methodology requested:

1. Data Cleaning & Financial Validation
2. Revenue & Profit Overview
3. Product & Category Profitability Analysis
4. Customer Contribution Analysis
5. Discount Impact Diagnostics
6. Market & Regional Profit Analysis
7. KPI Summary
8. Key Insights & Recommendations

The cleaned output of this notebook (`apl_clean.parquet` / `apl_clean.csv`) feeds the companion Streamlit dashboard (`dashboard/app.py`).
""")

# ---------------------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------------------
md("## 1. Setup & Imports")

code("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

pio.templates.default = "plotly_white"
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

# Fintech blue palette used consistently across all charts
PALETTE = ["#0B3D91", "#1D5FBF", "#3E8DED", "#7FB6F7", "#B7D8FB", "#0A2540"]
NEG_COLOR = "#D64545"
""")

code("""DATA_PATH = Path('../data/APL_Logistics.csv')
df_raw = pd.read_csv(DATA_PATH, encoding='latin1')
print(f"Rows: {df_raw.shape[0]:,}  |  Columns: {df_raw.shape[1]}")
df_raw.head()
""")

# ---------------------------------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------------------------------
md("""## 2. Data Cleaning & Financial Validation

Steps:
- Inspect nulls, duplicates, and data types
- Validate that financial fields (Sales, Benefit per order, Order Profit Per Order) are numeric and sensible
- Remove zero/invalid-value order records
- Normalize/derive a consistent `Profit Margin` field
""")

code("""# Null / duplicate audit
null_counts = df_raw.isnull().sum()
print("Columns with nulls:")
print(null_counts[null_counts > 0])
print(f"\\nDuplicate rows: {df_raw.duplicated().sum()}")
""")

code("""df = df_raw.copy()

# Drop exact duplicate order-item rows, if any
df = df.drop_duplicates()

# Financial validation: Sales and Order Item Total must be > 0 to represent a real transaction
before = len(df)
df = df[(df['Sales'] > 0) & (df['Order Item Total'] > 0) & (df['Order Item Quantity'] > 0)]
after = len(df)
print(f"Removed {before - after} zero/invalid-value order records ({before-after} rows)")

# Fill missing Customer Lname / Zipcode - not used in profitability math, keep as 'Unknown'/0
df['Customer Lname'] = df['Customer Lname'].fillna('Unknown')
df['Customer Zipcode'] = df['Customer Zipcode'].fillna(0)

# Derived, normalized profitability field (source of truth used throughout the notebook)
df['Profit Margin %'] = np.where(df['Sales'] != 0, (df['Benefit per order'] / df['Sales']) * 100, 0)

# Sanity clip: cap extreme outlier margins for visualization stability only (does not touch KPI totals)
df['Profit Margin % (clipped)'] = df['Profit Margin %'].clip(-100, 100)

print(f"\\nClean dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
df[['Sales', 'Benefit per order', 'Order Profit Per Order', 'Profit Margin %']].describe()
""")

# ---------------------------------------------------------------------------
# REVENUE & PROFIT OVERVIEW
# ---------------------------------------------------------------------------
md("""## 3. Revenue & Profit Overview

Compute headline revenue and profit figures, then compare trend and concentration patterns.
""")

code("""total_revenue = df['Sales'].sum()
total_profit = df['Benefit per order'].sum()
overall_margin = total_profit / total_revenue * 100
total_orders = df['Order Item Total'].count()
avg_order_value = df['Sales per customer'].mean()

print(f"Total Revenue        : ${total_revenue:,.2f}")
print(f"Total Profit         : ${total_profit:,.2f}")
print(f"Overall Profit Margin: {overall_margin:.2f}%")
print(f"Total Order Items    : {total_orders:,}")
print(f"Unique Customers     : {df['Customer Id'].nunique():,}")
print(f"Unique Products      : {df['Product Name'].nunique():,}")
""")

code("""# Revenue vs Profit by Shipping Mode (proxy trend view - dataset has no order date column)
ship_perf = df.groupby('Shipping Mode').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Benefit per order', 'sum'),
    Orders=('Order Item Total', 'count')
).reset_index()
ship_perf['Margin %'] = ship_perf['Profit'] / ship_perf['Revenue'] * 100
ship_perf = ship_perf.sort_values('Revenue', ascending=False)

fig = go.Figure()
fig.add_bar(x=ship_perf['Shipping Mode'], y=ship_perf['Revenue'], name='Revenue', marker_color=PALETTE[1])
fig.add_bar(x=ship_perf['Shipping Mode'], y=ship_perf['Profit'], name='Profit', marker_color=PALETTE[4])
fig.update_layout(barmode='group', title='Revenue vs Profit by Shipping Mode', height=420)
fig.show()
ship_perf
""")

code("""# Profit concentration: cumulative share of profit by customer (Pareto view)
cust_profit = df.groupby('Customer Id')['Benefit per order'].sum().sort_values(ascending=False).reset_index()
cust_profit['cum_profit_share'] = cust_profit['Benefit per order'].cumsum() / cust_profit['Benefit per order'].sum() * 100
cust_profit['cust_rank_share'] = (np.arange(1, len(cust_profit)+1) / len(cust_profit)) * 100

top10pct_cutoff = int(len(cust_profit) * 0.10)
share_from_top10pct = cust_profit.iloc[:top10pct_cutoff]['Benefit per order'].sum() / total_profit * 100
print(f"Top 10% of customers ({top10pct_cutoff:,} customers) generate {share_from_top10pct:.1f}% of total profit")

fig = px.line(cust_profit, x='cust_rank_share', y='cum_profit_share',
              title='Profit Concentration Curve (Pareto) — Customers Ranked by Profit',
              labels={'cust_rank_share': '% of Customers', 'cum_profit_share': 'Cumulative % of Profit'})
fig.update_traces(line_color=PALETTE[0], line_width=3)
fig.add_shape(type='line', x0=0, y0=0, x1=100, y1=100, line=dict(dash='dot', color='#999'))
fig.update_layout(height=420)
fig.show()
""")

# ---------------------------------------------------------------------------
# PRODUCT & CATEGORY PROFITABILITY
# ---------------------------------------------------------------------------
md("""## 4. Product & Category Profitability Analysis

Analyze margin by Product Name and Category Name; flag high-revenue/low-margin products and any loss-making categories.
""")

code("""cat_perf = df.groupby('Category Name').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Benefit per order', 'sum'),
    Orders=('Order Item Total', 'count')
).reset_index()
cat_perf['Margin %'] = cat_perf['Profit'] / cat_perf['Revenue'] * 100
cat_perf = cat_perf.sort_values('Revenue', ascending=False)

fig = px.bar(cat_perf.head(15), x='Revenue', y='Category Name', orientation='h',
             color='Margin %', color_continuous_scale=['#D64545', '#B7D8FB', '#0B3D91'],
             title='Top 15 Categories: Revenue Sized, Margin Colored')
fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=520)
fig.show()

loss_making = cat_perf[cat_perf['Profit'] < 0]
print(f"Loss-making categories: {len(loss_making)}")
low_margin = cat_perf[cat_perf['Margin %'] < cat_perf['Margin %'].median()].sort_values('Revenue', ascending=False)
print("\\nHigh-revenue but below-median-margin categories (watch list):")
low_margin.head(8)
""")

code("""prod_perf = df.groupby('Product Name').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Benefit per order', 'sum'),
    Orders=('Order Item Total', 'count')
).reset_index()
prod_perf['Margin %'] = prod_perf['Profit'] / prod_perf['Revenue'] * 100

print("Top 10 products by revenue:")
display(prod_perf.sort_values('Revenue', ascending=False).head(10))

print("\\nHigh-revenue, low-margin products (bottom-quartile margin among top-revenue quartile):")
top_rev_q = prod_perf['Revenue'].quantile(0.75)
low_margin_q = prod_perf['Margin %'].quantile(0.25)
flagged = prod_perf[(prod_perf['Revenue'] >= top_rev_q) & (prod_perf['Margin %'] <= low_margin_q)]
flagged.sort_values('Revenue', ascending=False)
""")

code("""fig = px.scatter(prod_perf, x='Revenue', y='Margin %', size='Orders', color='Margin %',
                  color_continuous_scale=['#D64545', '#B7D8FB', '#0B3D91'],
                  hover_name='Product Name',
                  title='Product Positioning: Revenue vs Profit Margin')
fig.add_hline(y=0, line_dash='dot', line_color='#666')
fig.update_layout(height=480)
fig.show()
""")

# ---------------------------------------------------------------------------
# CUSTOMER CONTRIBUTION
# ---------------------------------------------------------------------------
md("""## 5. Customer Contribution Analysis

Aggregate sales and profit by Customer Id, identify high-value vs low-margin/loss-making customers, and segment into value tiers.
""")

code("""cust_perf = df.groupby('Customer Id').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Benefit per order', 'sum'),
    Orders=('Order Item Total', 'count'),
    Segment=('Customer Segment', 'first')
).reset_index()
cust_perf['Margin %'] = cust_perf['Profit'] / cust_perf['Revenue'] * 100

print("Top 10 customers by profit:")
display(cust_perf.sort_values('Profit', ascending=False).head(10))

print("\\nBottom 10 customers by profit (lowest-margin / loss-making):")
cust_perf.sort_values('Profit', ascending=True).head(10)
""")

code("""# Value tier segmentation via profit quartiles
cust_perf['Value Tier'] = pd.qcut(cust_perf['Profit'], 4, labels=['Bronze (Q1)', 'Silver (Q2)', 'Gold (Q3)', 'Platinum (Q4)'])

tier_summary = cust_perf.groupby('Value Tier', observed=True).agg(
    Customers=('Customer Id', 'count'),
    Revenue=('Revenue', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()
tier_summary['Avg Margin %'] = tier_summary['Profit'] / tier_summary['Revenue'] * 100

fig = px.bar(tier_summary, x='Value Tier', y='Profit', color='Value Tier',
             color_discrete_sequence=PALETTE, title='Total Profit Contribution by Customer Value Tier')
fig.update_layout(showlegend=False, height=420)
fig.show()
tier_summary
""")

code("""seg_perf = df.groupby('Customer Segment').agg(
    Revenue=('Sales', 'sum'), Profit=('Benefit per order', 'sum'), Customers=('Customer Id', 'nunique')
).reset_index()
seg_perf['Margin %'] = seg_perf['Profit'] / seg_perf['Revenue'] * 100

fig = px.pie(seg_perf, names='Customer Segment', values='Revenue', hole=0.55,
             color_discrete_sequence=PALETTE, title='Revenue Share by Customer Segment')
fig.show()
seg_perf
""")

# ---------------------------------------------------------------------------
# DISCOUNT IMPACT
# ---------------------------------------------------------------------------
md("""## 6. Discount Impact Diagnostics

Compare margins with/without discounting, analyze discount rate vs profit ratio, and identify the discount threshold where margin erosion accelerates.
""")

code("""# Bucket discount rates and inspect resulting profit ratio
df['Discount Bucket'] = pd.cut(df['Order Item Discount Rate'],
                                bins=[-0.001, 0.0, 0.05, 0.10, 0.15, 0.20, 1.0],
                                labels=['0%', '0-5%', '5-10%', '10-15%', '15-20%', '20%+'])

disc_perf = df.groupby('Discount Bucket', observed=True).agg(
    Orders=('Order Item Total', 'count'),
    AvgProfitRatio=('Order Item Profit Ratio', 'mean'),
    Revenue=('Sales', 'sum'),
    Profit=('Benefit per order', 'sum')
).reset_index()
disc_perf['Margin %'] = disc_perf['Profit'] / disc_perf['Revenue'] * 100

fig = px.bar(disc_perf, x='Discount Bucket', y='Margin %', color='Margin %',
             color_continuous_scale=['#D64545', '#B7D8FB', '#0B3D91'],
             title='Profit Margin by Discount Rate Bucket — Erosion Threshold View')
fig.update_layout(height=420)
fig.show()
disc_perf
""")

code("""corr = df[['Order Item Discount Rate', 'Order Item Profit Ratio']].corr().iloc[0, 1]
print(f"Correlation between Discount Rate and Profit Ratio: {corr:.3f}")

fig = px.scatter(df.sample(min(8000, len(df)), random_state=42),
                  x='Order Item Discount Rate', y='Order Item Profit Ratio',
                  trendline='ols', opacity=0.35,
                  color_discrete_sequence=[PALETTE[1]],
                  title='Discount Rate vs Profit Ratio (sampled orders + trend line)')
fig.update_layout(height=460)
fig.show()
""")

# ---------------------------------------------------------------------------
# MARKET & REGIONAL
# ---------------------------------------------------------------------------
md("""## 7. Market & Regional Profit Analysis

Compare profitability across Markets, Order Regions, and Countries; flag high-revenue/weak-profit markets.
""")

code("""market_perf = df.groupby('Market').agg(
    Revenue=('Sales', 'sum'), Profit=('Benefit per order', 'sum'), Orders=('Order Item Total', 'count')
).reset_index()
market_perf['Margin %'] = market_perf['Profit'] / market_perf['Revenue'] * 100
market_perf = market_perf.sort_values('Revenue', ascending=False)

fig = go.Figure()
fig.add_bar(x=market_perf['Market'], y=market_perf['Revenue'], name='Revenue', marker_color=PALETTE[1], yaxis='y')
fig.add_trace(go.Scatter(x=market_perf['Market'], y=market_perf['Margin %'], name='Margin %',
                          yaxis='y2', mode='lines+markers', line=dict(color=NEG_COLOR, width=3)))
fig.update_layout(
    title='Market Revenue vs Profit Margin',
    yaxis=dict(title='Revenue ($)'),
    yaxis2=dict(title='Margin %', overlaying='y', side='right'),
    height=460
)
fig.show()
market_perf
""")

code("""region_perf = df.groupby('Order Region').agg(
    Revenue=('Sales', 'sum'), Profit=('Benefit per order', 'sum')
).reset_index()
region_perf['Margin %'] = region_perf['Profit'] / region_perf['Revenue'] * 100
region_perf = region_perf.sort_values('Revenue', ascending=False)

fig = px.bar(region_perf, x='Order Region', y='Revenue', color='Margin %',
             color_continuous_scale=['#D64545', '#B7D8FB', '#0B3D91'],
             title='Revenue by Order Region, Colored by Margin %')
fig.update_layout(xaxis={'categoryorder': 'total descending'}, height=460)
fig.show()

print("Countries: revenue-strong but margin-weak (bottom-quartile margin, top-half revenue):")
country_perf = df.groupby('Order Country').agg(Revenue=('Sales', 'sum'), Profit=('Benefit per order', 'sum')).reset_index()
country_perf['Margin %'] = country_perf['Profit'] / country_perf['Revenue'] * 100
rev_median = country_perf['Revenue'].median()
margin_q1 = country_perf['Margin %'].quantile(0.25)
country_perf[(country_perf['Revenue'] >= rev_median) & (country_perf['Margin %'] <= margin_q1)].sort_values('Revenue', ascending=False).head(10)
""")

# ---------------------------------------------------------------------------
# KPI SUMMARY
# ---------------------------------------------------------------------------
md("""## 8. Key Performance Indicator (KPI) Summary
""")

code("""kpi_summary = pd.DataFrame({
    'KPI': ['Total Revenue', 'Total Profit', 'Profit Margin (%)', 'Avg Sales per Customer',
            'Customer Value Index (Avg Profit/Customer)', 'Best Category Margin (%)',
            'Worst Category Margin (%)', 'Late Delivery Risk Rate (%)'],
    'Value': [
        f"${total_revenue:,.0f}",
        f"${total_profit:,.0f}",
        f"{overall_margin:.2f}%",
        f"${df['Sales per customer'].mean():,.2f}",
        f"${cust_perf['Profit'].mean():,.2f}",
        f"{cat_perf['Margin %'].max():.2f}%",
        f"{cat_perf['Margin %'].min():.2f}%",
        f"{df['Late_delivery_risk'].mean()*100:.1f}%"
    ]
})
kpi_summary
""")

code("""# Persist cleaned dataset + key aggregates for the Streamlit dashboard
out_dir = Path('../data')
df.to_parquet(out_dir / 'apl_clean.parquet', index=False)
df.to_csv(out_dir / 'apl_clean.csv', index=False)
print("Saved cleaned dataset to data/apl_clean.parquet and data/apl_clean.csv")
print(f"Final shape: {df.shape}")
""")

# ---------------------------------------------------------------------------
# INSIGHTS
# ---------------------------------------------------------------------------
md("""## 9. Key Insights & Recommendations

**Profitability is heavily concentrated.** A small share of top customers by profit account for a disproportionate share of total profit — the Pareto curve above quantifies this concentration precisely for this dataset. Retention and account-management investment should prioritize the Platinum/Gold value tiers identified in the customer segmentation.

**Revenue leadership does not equal margin leadership.** The top-revenue categories (Fishing, Cleats, Camping & Hiking, Cardio Equipment) are not necessarily the highest-margin ones. The revenue-vs-margin scatter and the "high-revenue but below-median-margin" watch list should guide pricing review, not just sales volume targets.

**Discounting shows a measurable margin cost.** The discount-rate vs profit-ratio relationship is negative — as discount buckets increase, average margin declines. The bucketed view highlights the rate at which erosion accelerates and gives a data-backed ceiling for discount policy.

**Markets and regions carry different risk/reward profiles.** Some markets post strong revenue with comparatively thinner margins; regional/country tables above flag the specific markets and countries that are revenue-heavy but margin-light, which is where commercial terms (freight allocation, discount caps, contract pricing) should be renegotiated first.

**Recommended next actions for leadership:**
1. Build account plans for Platinum/Gold-tier customers; investigate root causes for Bronze-tier / loss-making accounts (are they early-stage, discount-heavy, or high-return?).
2. Review pricing and discount policy for the flagged high-revenue/low-margin products and categories.
3. Cap or restructure discounts above the erosion threshold identified in the discount diagnostics.
4. Prioritize commercial-term renegotiation in the revenue-strong, margin-weak markets/countries.

These findings, and the interactive filters to explore them by segment/category/market/discount, are available in the companion Streamlit dashboard: `dashboard/app.py`.
""")

nb['cells'] = cells

with open('notebook/APL_Profitability_Analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook written.")
