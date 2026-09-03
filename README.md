# 🚚 Customer, Product & Profitability Performance Analysis
### APL Logistics (KWE Group) | Unified Mentor Internship Project

> **Turning supply chain data into commercial intelligence by identifying which customers, products, categories, and markets truly create profitable business value.**

---

## 📌 Project Overview

For a global logistics organization, high revenue does not always mean high profitability.

This project analyzes customer, product, discount, and market performance to answer an important business question:

> **Which customers, products, and regions truly generate value for the business?**

The project transforms large-scale logistics and sales data into actionable profitability insights, helping decision-makers move from a **revenue-focused approach** to a **profit-driven strategy**.

---

## 🎯 Business Problem

Organizations often have access to extensive sales and operational data but lack clear visibility into:

- 💰 Which customers generate the highest profit
- 📦 Which products and categories create sustainable margins
- 📉 How discounts affect profitability
- 👥 Which customers are high-value or low-value
- 🌍 Which markets and regions generate the strongest business value

As a result, business strategies may become revenue-focused but profit-blind.

This project provides a structured analytical solution to uncover customer value, product profitability, discount-driven margin erosion, and market-level performance.

---

# 🧠 Project Objectives

The analysis focuses on the following key business areas:

### 👥 Customer Value Analysis

Identify high-value customers and analyze profit concentration across the customer base.

### 📦 Product & Category Performance

Evaluate revenue, profit, and margins across products and categories.

### 💸 Discount Impact Analysis

Investigate how discount rates influence profitability and contribute to margin erosion.

### 🌍 Market & Regional Profitability

Compare financial performance across markets, regions, and geographical segments.

### 📊 Revenue & Profit Intelligence

Provide an executive-level overview of overall financial and profitability performance.

---

# 📁 Project Structure

```text
APL_Logistics_Profitability_Project/
│
├── dashboard/
│   │
│   ├── data/
│   │   └── apl_clean.parquet
│   │
│   ├── dashboard_app.py
│   └── requirements.txt
│
├── data/
│   └── apl_clean.parquet
│
├── notebook/
│   ├── APL_Profitability_Analysis.ipynb
│   └── build_notebook.py
│
├── APL_Profitability_Analysis.ipynb
├── README.md
├── dashboard_app.py
└── requirements.txt
```

---

# 📊 Dataset

The project analyzes a large-scale logistics and sales dataset containing:

- **180,519 order records**
- **40 original variables**
- **20,652 unique customers**
- **118 unique products**

The dataset includes information related to:

- Customer details
- Product and category information
- Sales and revenue
- Profit and profitability ratios
- Discounts
- Shipping modes
- Delivery performance
- Markets and regions

## ⚠️ Dataset Note

The original raw dataset is large and is not included in this repository.

For efficient analysis and dashboard performance, the project uses the cleaned dataset:

```text
apl_clean.parquet
```

The cleaned Parquet dataset is used by the Streamlit dashboard for faster loading and better performance.

---

# 🔬 Analytical Methodology

The project follows a structured end-to-end analytics workflow.

## 1️⃣ Data Cleaning & Financial Validation

The first stage focuses on preparing reliable data for analysis.

Key activities include:

- Validating sales and profit fields
- Checking missing values
- Identifying inconsistent records
- Preparing financial metrics
- Creating a cleaned dataset for analysis
- Exporting the optimized dataset in Parquet format

---

## 2️⃣ Revenue & Profit Overview

The financial overview evaluates the organization's overall business performance.

Key metrics include:

- Total Revenue
- Total Profit
- Overall Profit Margin
- Total Order Items
- Unique Customers
- Revenue and Profit by Shipping Mode

---

## 3️⃣ Product & Category Profitability Analysis

This analysis evaluates:

- Revenue by product category
- Profit by product category
- Category-level profit margins
- Product-level profitability
- High-revenue but potentially low-margin areas
- Loss-making categories

The objective is to identify where sales performance translates into meaningful profitability.

---

## 4️⃣ Customer Contribution Analysis

Customer-level analysis identifies:

- High-value customers
- Low-performing customers
- Revenue contribution
- Profit contribution
- Customer profitability concentration

A Pareto analysis was also performed to understand how profit is distributed across customers.

### Key Insight

The **top 10% of customers generate approximately 49.1% of total profit**, highlighting the importance of customer retention and strategic relationship management.

---

## 5️⃣ Discount Impact Diagnostics

Discount analysis investigates:

- Discount rate versus profitability
- Margin erosion caused by discounting
- High-discount scenarios
- Revenue versus profit trade-offs
- The relationship between discounts and profit ratios

The objective is to identify when discounting supports growth and when it begins to reduce business value.

---

## 6️⃣ Market & Regional Profit Analysis

Profitability is compared across:

- Markets
- Order Regions
- Countries

This helps identify areas where:

- Revenue and profit are both strong
- Revenue is high but margins are weak
- Commercial strategies may require optimization

---

# 📈 Key Performance Indicators

| KPI | Description |
|---|---|
| 💰 Total Revenue | Total sales generated across all orders |
| 📈 Total Profit | Aggregate profit generated across orders |
| 📊 Profit Margin | Profit as a percentage of total revenue |
| 👥 Unique Customers | Number of distinct customers |
| 📦 Product Performance | Revenue and profit contribution by products |
| 🏷️ Category Margin | Profitability across product categories |
| 💸 Discount Impact | Effect of discounting on profit margins |
| 🌍 Market Performance | Financial performance across markets and regions |

---

# 📊 Key Financial Results

| Metric | Result |
|---|---:|
| 💰 Total Revenue | **$36,784,734.31** |
| 📈 Total Profit | **$3,966,902.97** |
| 📊 Overall Profit Margin | **10.78%** |
| 📦 Total Order Items | **180,519** |
| 👥 Unique Customers | **20,652** |
| 📦 Unique Products | **118** |

---

# 🚚 Shipping Mode Performance

The analysis also evaluates financial performance across shipping modes.

| Shipping Mode | Revenue | Profit | Profit Margin |
|---|---:|---:|---:|
| Standard Class | $22,022,391.46 | $2,370,454.45 | 10.76% |
| Second Class | $7,145,444.68 | $750,308.17 | 10.50% |
| First Class | $5,674,369.65 | $643,121.92 | 11.33% |
| Same Day | $1,942,528.52 | $203,018.43 | 10.45% |

---

# 📦 Product & Category Insights

The analysis identifies category-level financial performance.

### High-Revenue Categories

- **Fishing**
  - Revenue: **$6,929,653.50**
  - Profit: **$756,220.76**
  - Profit Margin: **10.91%**

- **Camping & Hiking**
  - Revenue: **$4,118,425.42**
  - Profit: **$427,455.57**
  - Profit Margin: **10.38%**

The analysis found **no loss-making categories** in the evaluated category-level results.

---

# 💡 Key Insights

### 🔹 Revenue Does Not Always Equal Profitability

High sales alone are not sufficient for evaluating business performance. Profit and margin analysis provides a clearer picture of value creation.

### 🔹 Customer Profitability Is Concentrated

A relatively small percentage of customers contributes a significant portion of total profit.

### 🔹 Product Performance Varies

Products and categories can generate very different levels of revenue, profit, and margins.

### 🔹 Discounts Require Strategic Control

Discounting can increase sales volume while simultaneously reducing profit margins.

### 🔹 Market-Level Analysis Supports Better Decisions

Geographical and market analysis helps identify where commercial performance is strongest and where strategies may require improvement.

---

# 🖥️ Interactive Streamlit Dashboard

The project includes an interactive **Streamlit dashboard** that converts the analytical findings into an accessible decision-support application.

The dashboard enables users to explore profitability dynamically through interactive filters and visualizations.

---

## 📊 Dashboard Modules

### 💰 Revenue & Profit Overview

Provides a high-level view of:

- Total Revenue
- Total Profit
- Profit Margin
- Customer Count
- Revenue and Profit comparisons
- Shipping Mode Performance

---

### 👥 Customer Value Dashboard

Allows users to explore:

- Top customers by profit
- Bottom-performing customers
- Customer segment contribution
- Customer profitability distribution
- Profit concentration

---

### 📦 Product & Category Performance

Analyzes:

- Category profitability
- Product-level performance
- Revenue versus profit relationships
- Profit margin comparisons
- High-performing business areas

---

### 💸 Discount Impact Analyzer

Helps users understand:

- Discount versus profitability
- Discount rate versus profit ratio
- Margin erosion
- Financial impact of discounting

---

# 🎛️ Interactive Filters

The dashboard provides interactive filtering based on:

- Customer Segment
- Market
- Order Region
- Product Category
- Discount Rate

These filters allow users to explore profitability from multiple business perspectives.

---

# 🚀 Run the Project Locally

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
```

## 2️⃣ Navigate to the Project

```bash
cd APL_Logistics_Profitability_Project
```

## 3️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

## 4️⃣ Run the Streamlit Dashboard

```bash
streamlit run dashboard_app.py
```

Alternatively, if running from the dashboard folder:

```bash
cd dashboard
pip install -r requirements.txt
streamlit run dashboard_app.py
```

The Streamlit application will automatically open in your browser.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming and analysis |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical analysis |
| Plotly | Interactive data visualization |
| Streamlit | Interactive analytics dashboard |
| Jupyter Notebook | Exploratory data analysis |
| Parquet | Efficient data storage |

---

# 📚 Project Deliverables

This project includes:

- 📊 Exploratory Data Analysis (EDA)
- 📈 Customer Profitability Analysis
- 📦 Product & Category Performance Analysis
- 💸 Discount Impact Diagnostics
- 🌍 Market & Regional Profit Analysis
- 🧠 Business Insights and Recommendations
- 🖥️ Interactive Streamlit Dashboard
- 📄 Research Paper
- 🏛️ Executive Summary for Stakeholders

---

# 🎯 Business Recommendations

Based on the analysis, the following strategic actions are recommended:

### 1. Prioritize High-Value Customers

Focus customer retention and relationship strategies on customers who generate sustainable profit rather than high revenue alone.

### 2. Monitor High-Revenue, Low-Margin Products

Review products with strong sales but weak profitability to identify pricing, cost, or discount optimization opportunities.

### 3. Establish Discount Controls

Monitor discount rates and evaluate their financial impact before applying aggressive pricing strategies.

### 4. Measure Profit Alongside Revenue

Revenue should not be the only performance metric. Profit and profit margin should be included in customer, product, and market evaluations.

### 5. Strengthen High-Performing Markets

Invest strategically in markets and regions that consistently generate strong profitability.

### 6. Monitor Customer Concentration Risk

Since a significant proportion of profit is generated by a relatively small group of customers, businesses should monitor dependency risk and strengthen their broader customer base.

---

# 📄 Research Paper

The project research paper includes:

- Exploratory Data Analysis
- Financial performance evaluation
- Customer profitability insights
- Product and category analysis
- Discount impact analysis
- Market and regional analysis
- Business recommendations

The research component converts technical analysis into structured business insights.

---

# 🏛️ Executive Summary

The project also provides an executive-level summary designed to communicate key findings and recommendations clearly to stakeholders.

The summary focuses on:

- Overall financial performance
- Customer value
- Product profitability
- Discount-related risks
- Market performance
- Strategic recommendations

---

# 🎯 Business Impact

This project demonstrates how supply chain data can support **commercial intelligence**, rather than only operational monitoring.

Instead of asking only:

> **How much are we selling?**

The analysis helps decision-makers ask:

> **How profitably are we selling, who creates the most value, and where should the business focus next?**

By combining customer value, product profitability, discount diagnostics, and geographical performance, the project provides a comprehensive view of business value creation.

---

# 👩‍💻 Author

**Panthini Patel**

Aspiring **Data Scientist | AI Engineer | Data Analytics Enthusiast**

### Unified Mentor Internship Project

---

# ⭐ Project Vision

> **Transforming supply chain data into actionable profitability intelligence—helping organizations identify not just where revenue comes from, but where real business value is created.**

---

⭐ If you found this project interesting, consider giving the repository a star!
