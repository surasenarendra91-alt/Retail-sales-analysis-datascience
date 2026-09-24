# Retail Sales Analysis — Real-World Data Project

**Domain:** Retail &nbsp;|&nbsp; **Type:** End-to-End Data Analysis & Predictive Modeling

A complete applied data science project analyzing two years of multi-region retail transaction
data — from raw data through exploratory analysis, visualization, and machine learning–based
prediction — packaged as a portfolio-ready deliverable.

---

## What's Inside

```
project/
├── README.md                                  ← you are here
├── data/
│   ├── retail_sales_dataset.csv                ← 6,500-row transaction dataset
│   └── generate_dataset.py                     ← reproducible data generation script
├── notebooks/
│   ├── Retail_Sales_Analysis.ipynb             ← ⭐ main notebook (fully executed, charts inline)
│   ├── build_notebook.py                       ← script that builds the notebook
│   └── analysis.py                             ← standalone analysis + chart export script
├── visuals/
│   └── 01–10 …png                              ← 10 high-resolution exported charts
└── report/
    ├── Retail_Sales_Analysis_Report.docx       ← ⭐ 10-page formatted Word report
    ├── key_findings.txt                        ← raw KPI/finding values used in the report
    └── build_report.js                         ← script that builds the Word report
```

**Start here:** open `notebooks/Retail_Sales_Analysis.ipynb` for the full interactive analysis,
or `report/Retail_Sales_Analysis_Report.docx` for a polished, presentation-ready write-up.

---

## Project Workflow

1. **Dataset** — A realistic synthetic retail dataset (6,500 orders, 2024–2025) across 5 regions,
   3 product categories, 3 customer segments, with seasonality built in (holiday-season spike).
2. **Exploratory Data Analysis** — Monthly trends, category & sub-category profitability, regional
   performance, customer segment behavior, discount-vs-margin relationship, correlation analysis.
3. **Predictive Modeling**
   - *Sales forecasting*: linear trend regression projecting the next 3 months.
   - *Profit prediction*: Random Forest Regressor predicting order-level profit from operational
     features (quantity, price, discount, category, region, segment, shipping mode), evaluated
     with R² and MAE on a held-out test set.
4. **Findings & Recommendations** — Business-actionable conclusions translated from the statistical
   and model-based results (discount caps, inventory timing, regional cost review, etc.).

## Key Results

| Metric | Value |
|---|---|
| Total Sales | £5,983,894 |
| Total Profit | £222,951 |
| Overall Margin | 3.7% |
| Avg. Order Value | £920.60 |
| Profit Model R² | 0.317 |
| Profit Model MAE | £80.41 |

## How to Reproduce

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter

# 1. Regenerate the dataset (optional — CSV is already included)
python data/generate_dataset.py

# 2. Run the full analysis + export charts
python notebooks/analysis.py

# 3. Open the interactive notebook
jupyter notebook notebooks/Retail_Sales_Analysis.ipynb
```

## Tools & Libraries

Python · pandas · NumPy · scikit-learn (LinearRegression, RandomForestRegressor) ·
matplotlib · seaborn · Jupyter · docx (report generation)

---
*Note: the dataset is synthetically generated for coursework/demo purposes, with realistic
distributions, seasonality, and noise modeled on typical multi-region retail operations.*
