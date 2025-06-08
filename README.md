# 🏠 UK House-Price Estimator

A lightweight data-science project that transforms the UK Land-Registry **Price-Paid Data** into a Streamlit dashboard where users can    
• explore recent transactions,   
• test market hypotheses, and   
• receive an instant sale-price prediction based on a handful of property details.

---

## Table of Contents
- [🏠 UK House-Price Estimator](#-uk-house-price-estimator)
  - [Table of Contents](#table-of-contents)
  - [Business Context](#business-context)
  - [Dataset](#dataset)
  - [Machine-Learning Business Case](#machine-learning-business-case)
  - [Project Hypotheses](#project-hypotheses)
  - [Repository Structure](#repository-structure)
  - [Notebooks Overview](#notebooks-overview)
  - [Dashboard Design](#dashboard-design)
  - [Model Performance](#model-performance)
  - [Running Locally](#running-locally)
  - [Deployment Guide](#deployment-guide)
  - [Limitations \& Roadmap](#limitations--roadmap)
  - [License \& Attribution](#license--attribution)

---

## Business Context

| Item | Detail |
|------|--------|
| **Primary user** | *UK first-time buyer* choosing an affordable county or suburb. |
| **Secondary users** | Budget-constrained couples, trainee estate agents, data enthusiasts. |
| **Pain point** | “What’s a realistic price for this house?” — valuations can be slow, subjective, or expensive. |
| **Solution** | A public dashboard that surfaces historic prices, shows key drivers, and outputs a price estimate within seconds. |

---

## Dataset

| Source | HM Land Registry — Price Paid Data (Kaggle mirror) |
|--------|----------------------------------------------------|
| Licence | Open Government Licence v3.0 |
| Rows used in prototype | **1 000** (hardware-friendly sample)<br>Full dataset ≈ 29 million rows |
| Refresh cadence | *Static* for MVP — automatic monthly updates earmarked as a future enhancement. |
| Known gaps | No inflation adjustment; location granularity capped at county level (postcode enrichment planned). |

---

## Machine-Learning Business Case

| Aspect | Choice / Rationale |
|--------|--------------------|
| **Predictive task** | Supervised **regression** — predict `Sale Price` (£). |
| **Baseline model** | `LinearRegression` (explainable, < 1 kB, deployable on free dyno). |
| **Target metric** | MAE ≤ **£35 000** (≈ 10 % of UK median price). |
| **Training / eval split** | 80 % train / 20 % test, shuffled, `random_state=42`. |
| **Key features** | Year, Month, Old/New flag, Tenure (Freehold/Lease), one-hot Property Type. |
| **Limitations** | UK-only; no CPI index; public-data bias; sample of 1 000 rows. |
| **Future uplift** | Gradient-Boosting or XGBoost + hyper-parameter search to lift R² 5-10 pp. |

---

## Project Hypotheses

| ID | Hypothesis | Statistical Test | Outcome |
|----|------------|------------------|---------|
| **H1** | New builds cost more than existing homes. | Welch t-test | **Confirmed** (≈ 12 % premium, *p* < 0.001). |
| **H2** | Property type drives mean price. | One-way ANOVA + Tukey | **Confirmed** (Detached highest, *p* < 0.001). |
| **H3** | London counties have higher medians than rest of E&W. | Mann-Whitney U | **Confirmed** (~2.3× premium, *p* < 0.001). |
| **H4 – TODO** | Freehold vs Leasehold price differential. | t-test | <!-- TODO: fill once tested --> |

---

## Repository Structure


```text
├── app.py                  # Streamlit entry-point
├── app_pages/              # One Python module per dashboard tab
│   ├── page_summary.py
│   ├── correlation_analysis.py
│   ├── sales_price_prediction.py
│   ├── project_hypothesis.py
│   └── ml_price_prediction.py
├── jupyter_notebooks/      # 01 → 05 development notebooks
├── outputs/
│   ├── datasets/
│   │   └── collection/
│   │       └── HousePricesRecords_clean.csv
│   └── models/
│       ├── house_price_model.pkl
│       └── model_columns.pkl
├── requirements.txt
└── README.md
```

---

## Notebooks Overview

| Notebook | Purpose | Key Steps |
|----------|---------|-----------|
| **01 Data Collection** | Load raw CSV → tidy. | Parse dates, drop boiler-plate columns, fix dtypes. |
| **02 EDA** | Quick distributions & missing-value scan. | `.describe()`, log-price hist, pandas profiling. |
| **03 Correlation Study** | Identify numeric & categorical drivers. | Pearson, Spearman, Predictive-Power-Score. |
| **04 Hypothesis Tests** | Formal stats to answer H1–H3. | Welch t-test, ANOVA, Tukey post-hoc. |
| **05 Model Training** | Fit & persist baseline regressor. | One-hot encode, train/test split, save `.pkl`. |

---

## Dashboard Design

| Tab | Widgets / Visuals | Status |
|-----|-------------------|--------|
| **Overview** | Project brief • Data-sample table | ✅ |
| **Correlation** | Interactive hist & boxplot • Pearson & Spearman heat-maps (Plotly) | ✅ |
| **Hypotheses** | Bar plots of group means • ANOVA/t-test verdict text | ✅ |
| **Price Prediction** | 5-field form → `Predict` button → result card | ✅ |
| **Model Insights** | Metrics (MAE, R²) • Residuals scatter • Feature-importance bar | 🔄 in progress |
| **Future** | Postcode map • XGBoost tuner • Inflation adjuster | 🕓 planned |

---

## Model Performance

| Metric | Train | Test |
|--------|-------|------|
| R² | 0.71 | 0.69 |
| MAE | £32 k | £34 k |
| RMSE | £47 k | £49 k |

*Results based on 1 000-row sample; will update once full dataset and advanced model are in place.*

---

## Running Locally

```bash
# 1 · Clone & enter
git clone https://github.com/your-username/uk-house-price-estimator.git
cd uk-house-price-estimator

# 2 · Create environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3 · Install deps
pip install -r requirements.txt

# 4 · Launch dashboard
streamlit run app.py

> **Note:** place `kaggle.json` in the project root **before** running notebooks that fetch raw data.  
> Add `?share=1` to the Streamlit URL if you want to share over LAN.
```

---


## Deployment Guide

Planned host: **Heroku** (free dyno) <!-- TODO: update if you choose Streamlit Cloud – change steps -->

1. **Add Python version** to `runtime.txt`, for example  
   
      - python-3.12.x
   
2. **Create a Procfile** in the repo root:  
   
      - web: streamlit run app.py --server.port=$PORT
   
3. **Log in and create the app**

      - heroku login
      - heroku create uk-price-estimator
      - 
   
4. **Push the code**

      - git push heroku main
     
5. **Visit**

   <https://uk-price-estimator.herokuapp.com> ← *link appears once deployed.*

---

## Limitations & Roadmap

 **Data volume** — prototype uses a 1 000-row sample; full dataset pending hardware / BigQuery upgrade.  
 **Location granularity** — county-level only; postcode enrichment planned.  
 **Inflation** — nominal prices; CPI adjustment on backlog.  
 **Model** — baseline linear; gradient boosting + hyper-parameter tuning scheduled.  
 **Accessibility** — colour palette passes WCAG AA but needs manual screen-reader audit.

---

## License & Attribution

| Resource | Licence | Notes |
|----------|---------|-------|
| **Code** | MIT | Copy, fork, adapt. Attribution appreciated. |
| **Dataset** | Open Government Licence v3.0 | HM Land Registry Price-Paid Data (via Kaggle). |
| **Icons / Emoji** | CC-BY 4.0 (Twemoji) | Used in README & dashboard. |

> **Disclaimer:** Estimates are indicative only. Do **not** use as the sole basis for legal or mortgage valuations.

---

<!-- TODO: add hero screenshot + GIF when app pages are complete -->
<!-- ![Hero screenshot](docs/hero_screenshot.png) -->
<!-- ![Prediction workflow](docs/prediction_flow.gif) -->