# 🏠 UK House-Price Estimator

A lightweight data-science project that transforms the UK Land-Registry **Price-Paid Data** into a Streamlit dashboard where users can  
- explore recent transactions  
- test market hypotheses  
- receive an instant sale-price prediction based on a handful of property details  

> **Live demo:** _TODO: add your deployed URL here_  
> **Data source:** HM Land Registry PPD via Kaggle — `inputs/datasets/raw/price_paid_records.csv`

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
- [1 · Clone \& enter](#1--clone--enter)
- [2 · Create \& activate venv](#2--create--activate-venv)
- [3 · Install dependencies](#3--install-dependencies)
- [4 · (Re)generate data \& model](#4--regenerate-data--model)
- [5 · Launch dashboard](#5--launch-dashboard)

---

## Business Context

| Item               | Detail                                                                             |
|--------------------|------------------------------------------------------------------------------------|
| **Primary user**   | Sarah, a first-time buyer in Kent, who wants a quick, data-driven price check.     |
| **Secondary users**| Budget-conscious couples, trainee estate agents, data enthusiasts.                 |
| **Pain point**     | “What’s a fair price for this house?” — valuations can be slow, subjective, costly.|
| **Solution**       | Public dashboard surfacing historic prices, key drivers, and instant estimates.    |

---

## Dataset

| Attribute            | Value                                                 |
|----------------------|-------------------------------------------------------|
| **Source**           | HM Land Registry Price-Paid Data (Kaggle mirror)      |
| **Licence**          | Open Government Licence v3.0                         |
| **Rows in prototype**| 1 000 (hardware-friendly sample)                      |
| **Full size**        | ≈ 29 million rows                                      |
| **Refresh cadence**  | Static for MVP (monthly auto-update planned)          |
| **Known gaps**       | No inflation adjustment; county-level only (postcodes TBD) |

---

## Machine-Learning Business Case

| Aspect               | Choice / Rationale                                                              |
|----------------------|---------------------------------------------------------------------------------|
| **Task**             | Supervised regression → predict sale price (£)                                   |
| **Baseline model**   | `LinearRegression` (explainable, <1 KB, fast on free dyno)                      |
| **Target metric**    | MAE ≤ £35 000 (~10% of UK median)                                               |
| **Split**            | 80% train / 20% test, `random_state=42`, shuffle                                |
| **Features**         | Year, Month, Old/New flag, Tenure (Freehold/Lease), one-hot Property_Type      |
| **Limitations**      | UK-only, no CPI, public-data bias, 1 000-row sample                             |
| **Future uplift**    | GradientBoosting/XGBoost + hyperparameter search → +5–10 pp R²                   |

---

## Project Hypotheses

| ID   | Hypothesis                                                   | Test                 | Result     |
|------|--------------------------------------------------------------|----------------------|------------|
| **H1** | New builds command a price premium vs. existing homes       | Welch’s t-test       | Confirmed  |
| **H2** | Detached/Semi/Terraced/Flat have different mean prices     | One-way ANOVA + Tukey| Confirmed  |
| **H3** | London counties > rest of England & Wales median prices    | Mann-Whitney U       | Confirmed  |
| **H4** | Freehold vs Leasehold price differential                   | Welch’s t-test       | TODO       |

---

## Repository Structure

```text
├── app.py                        # Streamlit entry point
├── app_pages/                    # Dashboard page modules
│   ├── page_summary.py
│   ├── correlation_analysis.py
│   ├── sales_price_prediction.py
│   ├── project_hypothesis.py
│   └── ml_price_prediction.py
├── jupyter_notebooks/            # 01 → 05 developmental notebooks
├── outputs/
│   ├── datasets/
│   │   └── collection/
│   │       └── HousePricesRecords_clean.csv
│   └── models/
│       ├── house_price_model.pkl
│       └── model_columns.pkl
├── requirements.txt
└── README.md

## Notebooks Overview

| Notebook | Purpose                                          | Key Steps                                |
|----------|--------------------------------------------------|------------------------------------------|
| 01 Data Collection     | Ingest & preview raw CSV                        | Parse dates, drop junk columns, inspect head |
| 02 Data Cleaning & EDA | Clean & examine distributions                   | Drop nulls, convert dtypes, histograms, dtypes |
| 03 Correlation Study   | Identify strong predictors                      | Pearson, Spearman, heatmaps, scatter plots |
| 04 Hypothesis Testing  | Statistically validate H1–H3                    | t-tests, ANOVA, Tukey post-hoc            |
| 05 Model Training      | Fit & save baseline regression model            | One-hot encoding, train/test split, joblib dump |

---

## Dashboard Design

| Tab                     | Contents                                                | Status       |
|-------------------------|---------------------------------------------------------|--------------|
| **Project Overview**    | Project brief, sample table, baseline metrics           | ✅ Ready     |
| **Correlation Analysis**| Interactive heatmaps & scatterplots                     | ✅ Ready     |
| **Hypothesis Validation** | Verdict text + supporting plots                       | ✅ Ready     |
| **Sale Price Prediction** | Input form → Predict button → estimate card           | ✅ Ready     |
| **Machine Learning Model**| Train/Test metrics, residuals, feature-importance chart| 🔄 In progress |

---

## Model Performance

| Metric | Train    | Test     |
|--------|----------|----------|
| R²     | 0.68     | 0.53     |
| MAE    | £64,788  | £69,667  |
| RMSE   | £119,844 | £118,120 |

*Based on 1 000-row prototype. Will update with full dataset & advanced model.*

---

## Running Locally

```bash
# 1 · Clone & enter
git clone https://github.com/your-username/uk-house-price-estimator.git
cd uk-house-price-estimator

# 2 · Create & activate venv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3 · Install dependencies
pip install -r requirements.txt

# 4 · (Re)generate data & model
jupyter notebook     # run 01 → 05 Note: place kaggle.json in project root before running any notebooks.

# 5 · Launch dashboard
streamlit run app.py
