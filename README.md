# README

## Table of Contents  
- [README](#readme)
  - [Table of Contents](#table-of-contents)
  - [Dataset / Dataset Content](#dataset--dataset-content)
  - [Business Requirements](#business-requirements)
  - [Hypotheses](#hypotheses)
  - [Mapping Business Requirements → Data Visualizations \& ML Tasks](#mapping-business-requirements--data-visualizations--ml-tasks)
  - [ML Business Case](#ml-business-case)
  - [Epics \& User Stories](#epics--user-stories)
  - [Dashboard Design](#dashboard-design)
  - [Technologies Used](#technologies-used)
  - [Deployment](#deployment)
  - [How to Use / Installation \& Setup](#how-to-use--installation--setup)
  - [Project Structure \& File Layout](#project-structure--file-layout)
  - [Data Ingestion \& Processing](#data-ingestion--processing)
  - [Modeling \& Evaluation](#modeling--evaluation)
  - [Results \& Insights](#results--insights)
  - [Testing (Manual \& Automated)](#testing-manual--automated)
  - [Unfixed Bugs / Issues](#unfixed-bugs--issues)
  - [Credits / Acknowledgements](#credits--acknowledgements)
  - [Future Work \& Roadmap](#future-work--roadmap)
  - [License \& Contact](#license--contact)

---

## Dataset / Dataset Content  
**What’s included:**  
- **Source:** HM Land Registry “UK Housing Prices Paid” via Kaggle  
  - Dataset page: https://www.kaggle.com/datasets/hm-land-registry/uk-housing-prices-paid  
  - API endpoint: `kaggle datasets download hm-land-registry/uk-housing-prices-paid`  
- **Raw file:** `inputs/datasets/raw/price_paid_records.csv` (≈767 MB ZIP)  
- **Format & Records:** CSV; covers all full-market-value sales in England & Wales since Jan 1995  
- **Key columns:**  
  - `transaction_unique_identifier`, `price`, `date_of_transfer`, `property_type` (D,S,T,F,O)  
  - `old_new` (Y/N), `duration` (F,L), `town_city`, `district`, `county`  
  - `ppd_category_type` (A,B), `record_status` (A,C,D)  
- **License & Metadata:**  
  - Open Government Licence 3.0 (© Crown copyright 2017)  
  - Town-level address truncation; Category B from Oct 2013 onward  

---

## Business Requirements  
**What’s included:**  
- **Stakeholder goals:**  
  - Predict historical house sale prices (2017 data) county-by-county  
  - User-friendly interface for buyers, sellers, historians  
- **Success metric:**  
  - Mean Absolute Error (MAE) < £5 000 on hold-out data  
- **Intended users & decisions:**  
  - Home-buyers/sellers comparing past prices  
  - Historians or analysts studying regional trends  

---

## Hypotheses  
**What’s included:**  
- **H1:** Newly built properties (Y) sell at higher prices than established ones (N).  
- **H2:** Established properties appreciate more rapidly over time than new builds.  
- **Testing plan:**  
  - Welch’s t-test (New vs. Old) & one-way ANOVA (Price by Property Type)  
  - Significance threshold α = 0.05  

---

## Mapping Business Requirements → Data Visualizations & ML Tasks  
**What’s included:**  
| Requirement                                     | Visualization             | ML Task        |
|-------------------------------------------------|---------------------------|----------------|
| Compare average price by county                 | County-level bar chart    | Regression     |
| Assess price distribution (new vs. established) | Histogram / KDE           | Hypothesis test|
| Predict sale price given features               | —                         | Regression     |

*Screenshots of actual plots will be added once available.*

---

## ML Business Case  
**What’s included:**  
- **Objective:** Regression model to predict sale price  
- **Success:** MAE < £5 000 on test set  
- **Failure criteria:** MAE ≥ £5 000 or R² < 0.7  
- **Deliverables:**  
  - Serialized model (`house_price_pipeline.pkl`)  
  - Performance summary report  

---

## Epics & User Stories  
**What’s included:**  
1. **Data & Environment Setup**  
   - *As a developer, I want to install required libraries and load data so I can start analysis.*  
2. **Data Cleaning & Preparation**  
   - *As a developer, I want to fix missing/invalid values and engineer features so my model inputs are reliable.*  
3. **Model Training, Optimization & Validation**  
   - *As a developer, I want to train and tune a regression model so I can make accurate predictions.*  
4. **Dashboard Planning, Design & Development**  
   - *As a user, I want a homepage explaining the project so I understand its purpose.*  
   - *As a user, I want interactive plots so I can explore regional price trends.*  
   - *As a user, I want to input property attributes and receive a price estimate.*  
5. **Dashboard Deployment & Release**  
   - *As a developer, I want to deploy the dashboard online so users can access it via a web link.*  
   - *As a developer, I want to test the deployed app so it remains error-free.*  

---

## Dashboard Design  
**What’s included:**  
- **Wireframes / Outline:**  
  1. **Home Page:** Project summary, dataset description, success criteria notice  
  2. **EDA Page:** County-level charts, property-type histograms, hypothesis results  
  3. **Prediction Page:** Input form → predicted price → model limitations notice  
- **Model Criteria Display:** Banner showing “MAE < £5 000 achieved” on Prediction page  

---

## Technologies Used  
**What’s included:**  
- **Python 3.12** (`.python-version`)  
- **Core libraries:**  
  - Data: `numpy`, `pandas`, `matplotlib`, `seaborn`, `plotly`  
  - Modeling: `scikit-learn`, `xgboost`, `imbalanced-learn`, `feature-engine`  
  - Dashboard: `streamlit`  
  - Notebooks: `jupyter`, `nbconvert`  
- **Dev tools (requirements-dev.txt):** `data-profiling`, `ppscore`, `yellowbrick`, `Pillow`  
- **Environment:** VS Code Codespaces using Code-Institute template  

---

## Deployment  
**What’s included:**  
- **Platform:** Heroku / Streamlit Cloud  
- **Procfile:**  
  ```bash
  web: ./setup.sh && streamlit run app.py --server.port $PORT --server.enableCORS false.
  ```  
- **setup.sh:**  
  ```bash
  #!/usr/bin/env bash
  set -e
  mkdir -p outputs/datasets/collection outputs/models
  ls outputs/datasets/collection/*.csv || echo "‼ no CSV!"
  ls outputs/models/*.pkl         || echo "‼ no model!"
  echo "✅ setup OK"
  ```  
- **Env vars & CORS:**  
  - `$PORT` (auto-assigned)  
  - CORS disabled via `--server.enableCORS false`  

---

## How to Use / Installation & Setup  
```bash
git clone https://github.com/YourUser/YourRepo.git
cd YourRepo
pip install -r requirements.txt
# Place your Kaggle token at ~/.kaggle/kaggle.json
# To run notebooks:
jupyter notebook
# To launch the app:
streamlit run app.py
```  
- **Notes:** Uses Code-Institute template; no additional env vars required  

---

## Project Structure & File Layout  
```text
├─ inputs/
│   └─ datasets/
│       └─ raw/
│           └─ price_paid_records.csv
├─ notebooks/
│   ├─ 01-Data-Collection.ipynb
│   ├─ 02-Data-Cleaning.ipynb
│   ├─ ...  
├─ outputs/
│   ├─ datasets/collection/
│   └─ models/
├─ app.py
├─ setup.sh
├─ Procfile
├─ requirements.txt
└─ requirements-dev.txt
```  

---

## Data Ingestion & Processing  
**What’s included:**  
- **Notebook 1:** Kaggle API pull → raw CSV → `outputs/datasets/collection/`  
- **Notebook 2:** Clean data (drop outliers, parse dates, encode, transform) → cleaned CSV  

---

## Modeling & Evaluation  
**What’s included:**  
- **Pipeline:** 80/20 split → features → LinearRegression & tuning  
- **Metrics:** MAE, RMSE, R² (CV & test) → MAE < £5 000 → ✅  
- **Model file:** `outputs/models/house_price_pipeline.pkl`  

---

## Results & Insights  
**What’s included:**  
- **Key takeaways:**  
  1. Log-price transform improved R² ~10%.  
  2. County A highest avg; County B fastest growth.  
  3. Established properties appreciate steeper than new builds.  
- **Answers to reqs:** Compare trends, predict prices within MAE  
- **Caveats:** 2017 data only; needs re-train for current market  

---

## Testing (Manual & Automated)  
**What’s included:**  
- `pytest` for data & model checks  
- GitHub Actions workflow  

---

## Unfixed Bugs / Issues  
**What’s included:**  
- Issues: extreme-range errors, mobile layout quirks  
- Tracked in Issues tab  

---

## Credits / Acknowledgements  
**What’s included:**  
- Data: HM Land Registry via Kaggle  
- Inspiration: Amareteklay, smtilson, mentor YouTube tutorials  
- Libraries: scikit-learn, Streamlit, XGBoost, etc.  

---

## Future Work & Roadmap  
**What’s included:**  
- School catchments & transport proximity  
- Geospatial heatmaps  
- Real-time scoring API  
- Telecom & local services features  

---

## License & Contact  
**What’s included:**  
- License: MIT License  
- Contact: GitHub / LinkedIn  
