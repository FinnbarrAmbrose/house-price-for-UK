# 📝 Project 5 – House-Price Estimator To-Do List

## 1 · Streamlit Dashboard

- [ ] **page_summary.py**
  - [ ] Replace hard-coded `MODEL_MAE / RMSE / R2` with an auto-load:
        - Save `model_metrics.json` during training.
        - Read JSON in `page_summary.py` and populate KPI cards.

- [ ] **correlation_analysis.py**
  - [ ] Histogram & boxplot of `Price` (Plotly)
  - [ ] Pearson & Spearman heat-maps (Plotly, interactive)
  - [ ] Dropdown / multiselect filters (Year, County)

- [ ] **sales_price_prediction.py**
  - [ ] 5-field input form (Year, Month, Old/New, Tenure, Property Type)
  - [ ] Load `house_price_model.pkl` + `model_columns.pkl`
  - [ ] Prediction output card (formatted £)
  - [ ] Display model MAE disclaimer
  - [ ] Optional Future Improvement: Convert this model into a full pipeline that includes encoding, so prediction becomes more flexible.

- [ ] **project_hypothesis.py**
  - [ ] Text summary of H1–H3 results + p-values
  - [ ] Bar plot of mean prices by group
  - [ ] Option to download ANOVA/t-test table

- [ ] **ml_price_prediction.py**
  - [ ] Residuals scatter (Actual vs Predicted)
  - [ ] Feature-importance bar chart (coefficients)
  - [ ] Button to show training metrics table

## 2 · Data & Modelling

- [ ] Save full cleaned dataset under `outputs/datasets/v1/`
- [ ] (Optional) Enrich with postcode → lat/lon lookup
- [ ] Implement gradient-boosting / XGBoost model
  - [ ] Hyper-parameter grid (≥ 6 params × 3 values for Distinction)
  - [ ] Re-evaluate metrics & update README
- [ ] Add H4 test (Freehold vs Leasehold) to `04_Hypothesis_Tests.ipynb`

## 3 · Documentation

- [ ] Insert hero screenshot in README (`docs/hero_screenshot.png`)
- [ ] Record & embed 5-sec GIF of prediction flow (`docs/prediction_flow.gif`)
- [ ] Replace TODO placeholders (live URL, screenshots, GIF)
- [ ] Switch asterisk lists to dash lists (markdownlint clean)
- [ ] Add `.markdownlint.json` if custom rules needed
- [ ] Update data-dictionary section once postcode added
- [ ] Add academic/blog references to README

## 4 · Deployment

- [ ] Create `runtime.txt` (e.g., `python-3.12.x`)
- [ ] Create `Procfile`  
      `web: streamlit run app.py --server.port=$PORT`
- [ ] Push to Heroku (or Streamlit Cloud)  
      `heroku create uk-price-estimator` → `git push heroku main`
- [ ] Confirm app loads at `<live-URL>` & paste link in README
- [ ] Store `kaggle.json` & any keys as Heroku config vars

## 5 · Extras for Merit / Distinction

- [ ] Interactive postcode heat-map page (Plotly/Mapbox)
- [ ] Four distinct interactive plots confirmed in dashboard
- [ ] Versioned data folders (`/v1/`, `/v2/`) – criterion 5.7
- [ ] Conclude whether new model meets improved MAE/R² target
- [ ] Prepare short CHANGELOG.md for final submission

