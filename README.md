# Customer, Product, and Profitability Performance Analysis — APL Logistics (KWE Group)

Unified Mentor project deliverables.

## Contents

```
apl_project/
├── data/
│   ├── APL_Logistics.csv        # original dataset (180,519 rows)
│   ├── apl_clean.csv            # cleaned dataset (notebook output)
│   └── apl_clean.parquet        # cleaned dataset, used by the dashboard
├── notebook/
│   └── APL_Profitability_Analysis.ipynb   # full EDA + methodology, pre-executed
└── dashboard/
    ├── app.py                   # Streamlit dashboard (fintech blue/white theme)
    ├── requirements.txt
    ├── .streamlit/config.toml   # theme config
    └── data/apl_clean.parquet   # local copy for the dashboard to read
```

## Notebook

`notebook/APL_Profitability_Analysis.ipynb` walks through the full methodology from the
project brief:

1. Data Cleaning & Financial Validation
2. Revenue & Profit Overview
3. Product & Category Profitability Analysis
4. Customer Contribution Analysis
5. Discount Impact Diagnostics
6. Market & Regional Profit Analysis
7. KPI Summary
8. Key Insights & Recommendations

It has already been executed end-to-end (no errors) and writes the cleaned dataset
to `data/apl_clean.parquet` / `.csv`, which the dashboard reads.

## Dashboard

Run locally:

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

Modules (tabs): Revenue & Profit Overview · Customer Value · Product & Category
Performance · Discount Impact Analyzer, each filterable by Customer Segment,
Market, Order Region, Category, and Discount Rate via the sidebar.
