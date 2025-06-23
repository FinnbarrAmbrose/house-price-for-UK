# 🏠 UK House-Price Estimator
> A lightweight Streamlit dashboard that transforms UK Land-Registry Price-Paid data into an interactive tool for exploring recent transactions, testing market hypotheses, and predicting sale prices.  
> **Live demo:** _TODO: add your deployed URL here_  
> **Data source:** HM Land Registry PPD via Kaggle — `inputs/datasets/raw/price_paid_records.csv` fileciteturn1file0

## Table of Contents
1. [Overview](#overview)  
2. [Getting Started](#getting-started)  
3. [Data](#data)  
4. [Approach](#approach)  
5. [Features & Architecture](#features--architecture)  
6. [Model Performance](#model-performance)  
7. [Usage](#usage)  
8. [Deployment](#deployment)  
9. [Testing](#testing)  
10. [Roadmap & Known Issues](#roadmap--known-issues)  
11. [Tech Stack](#tech-stack)  
12. [Contributing](#contributing)  
13. [License & Credits](#license--credits)

---

## Overview
**Primary user:** Sarah, a first-time buyer in Kent, who wants a quick, data-driven price check.  
**Secondary users:** Budget-conscious couples, trainee estate agents, data enthusiasts.  
**Pain point:** “What’s a fair price for this house?” — valuations can be slow, subjective, costly.  
**Solution:** Public dashboard surfacing historic prices, key drivers, and instant estimates. fileciteturn1file0

## Getting Started
**Prerequisites**  
- Python 3.x  
- pip, virtualenv  

**Installation**  
```bash
git clone https://github.com/your-username/uk-house-price-estimator.git
cd uk-house-price-estimator
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
``` fileciteturn1file0

## Data
- **Source:** HM Land Registry Price-Paid Data (Kaggle mirror)  
- **Licence:** Open Government Licence v3.0  
- **Prototype sample:** 1 000 rows (hardware-friendly)  
- **Full dataset:** ≈ 29 million rows  
- **Refresh cadence:** Static for MVP (monthly auto-update planned)  
- **Known gaps:** No inflation adjustment; county-level only (postcodes TBD) fileciteturn1file0

## Approach
**Task:** Supervised regression → predict sale price (£)  
**Baseline:** `LinearRegression` (explainable, < 1 KB, fast on free dyno)  
**Target metric:** MAE ≤ £35 000 (~ 10% of UK median)  
**Split:** 80% train / 20% test, `random_state=42`, shuffle  
**Features:** Year, Month, Old/New flag, Tenure (Freehold/Lease), one-hot Property_Type  
**Limitations:** UK-only; no CPI adjustment; public-data bias; 1 000-row sample  
**Future uplift:** GradientBoosting/XGBoost + hyperparameter search → + 5–10 pp R²

### Project Hypotheses
| ID  | Hypothesis                                               | Test                   | Status    |
|-----|----------------------------------------------------------|------------------------|-----------|
| H1  | New builds command a price premium vs. existing homes    | Welch’s t-test         | Confirmed |
| H2  | Detached/Semi/Terraced/Flat have different mean prices   | One-way ANOVA + Tukey  | Confirmed |
| H3  | London counties > rest of England & Wales median prices  | Mann-Whitney U         | Confirmed |
| H4  | Freehold vs Leasehold price differential                 | Welch’s t-test         | TODO      | fileciteturn1file0

## Features & Architecture
### Repository Structure
```text
├── app.py
├── app_pages/
│   ├── page_summary.py
│   ├── correlation_analysis.py
│   ├── sales_price_prediction.py
│   ├── project_hypothesis.py
│   └── ml_price_prediction.py
├── jupyter_notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   ├── 03_correlation_study.ipynb
│   ├── 04_hypothesis_testing.ipynb
│   └── 05_model_training.ipynb
├── inputs/datasets/raw/price_paid_records.csv
├── outputs/
│   ├── datasets/collection/HousePricesRecords_clean.csv
│   └── models/
│       ├── house_price_model.pkl
│       └── model_columns.pkl
└── requirements.txt
```

### Dashboard Design
| Tab                       | Contents                                             | Status       |
|---------------------------|------------------------------------------------------|--------------|
| Project Overview          | Brief summary, sample table, baseline metrics        | ✅ Ready     |
| Correlation Analysis      | Interactive heatmaps & scatterplots                  | ✅ Ready     |
| Hypothesis Validation     | Verdicts with supporting plots                       | ✅ Ready     |
| Price Prediction          | Input form → predict button → estimate card          | ✅ Ready     |
| ML Model Details          | Train/test metrics, residuals, feature‐importance     | 🔄 In Progress | fileciteturn1file0

## Model Performance
| Metric | Train    | Test     |
|--------|----------|----------|
| R²     | 0.68     | 0.53     |
| MAE    | £64,788  | £69,667  |
| RMSE   | £119,844 | £118,120 |

_*Based on 1 000-row prototype; to be updated with full dataset & advanced models._ fileciteturn1file0

## Usage
```bash
streamlit run app.py
```
- Open `http://localhost:8501`
- Navigate via sidebar fileciteturn1file0

## Deployment
**Option 1: Heroku**
1. Ensure `Procfile` and `runtime.txt` are present at project root.
2. Log in: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push code: `git push heroku main`
5. Scale dyno: `heroku ps:scale web=1`
6. Open app: `heroku open`

**Option 2: Streamlit Community Cloud**
1. Commit & push your repo to GitHub.
2. Go to https://share.streamlit.io and select your repository.
3. Choose branch & main file (`app.py`).
4. Click Deploy & share your live link. fileciteturn1file0

## Testing
- **Manual:** Follow user stories in dashboard
- **Automated:** (If available) run `pytest` in `/tests` fileciteturn1file0

## Roadmap & Known Issues
- **Bugs:** Occasional date-parsing warnings in notebooks fileciteturn1file0

## Tech Stack
- **Languages:** Python
- **Framework:** Streamlit
- **ML Libraries:** scikit-learn, XGBoost, ppscore
- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn fileciteturn1file0

## Contributing
1. Fork the repo
2. Create a feature branch
3. Submit a pull request with clear description fileciteturn1file0

## License & Credits
MIT © Your Name  
Data source: HM Land Registry PPD (Kaggle mirror)  
Inspired by UK house-price modeling examples fileciteturn1file0
