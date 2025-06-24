#!/usr/bin/env bash
set -euo pipefail

echo "📝 Running all notebooks…"

# Ensure output directories exist
mkdir -p output
mkdir -p models

# 1) Data Collection
jupyter nbconvert \
  --to notebook \
  --execute "notebooks/01 - Data Collection-1.ipynb" \
  --output "output/01_Data_Collection_out.ipynb"

# 2) Data Cleaning
jupyter nbconvert \
  --to notebook \
  --execute "notebooks/02_data_cleaning (1).ipynb" \
  --output "output/02_Data_Cleaning_out.ipynb"

# 3) Exploratory Data Analysis
jupyter nbconvert \
  --to notebook \
  --execute "notebooks/03 - Exploratory Data Analysis.ipynb" \
  --output "output/03_EDA_out.ipynb"

# 4) Hypothesis Testing
jupyter nbconvert \
  --to notebook \
  --execute "notebooks/04 - Hypothesis Testing.ipynb" \
  --output "output/04_Hypothesis_Testing_out.ipynb"

# 5) Model Training & Evaluation
jupyter nbconvert \
  --to notebook \
  --execute "notebooks/05_Model_Training_and_Evaluation.ipynb" \
  --output "output/05_Model_Training_out.ipynb"

echo "✅ All notebooks complete. Launching app…"

exec streamlit run app.py
