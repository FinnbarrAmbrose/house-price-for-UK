#!/usr/bin/env bash
set -e

echo "📝 Running all notebooks…"

jupyter nbconvert \
  --to notebook --execute notebooks/"01 - Data Collection-1.ipynb" \
  --output output/"01_Data_Collection_out.ipynb"

jupyter nbconvert \
  --to notebook --execute notebooks/"02_data_cleaning (1).ipynb" \
  --output output/"02_Data_Cleaning_out.ipynb"

jupyter nbconvert \
  --to notebook --execute notebooks/"03 - Exploratory Data Analysis.ipynb" \
  --output output/"03_EDA_out.ipynb"

jupyter nbconvert \
  --to notebook --execute notebooks/"04 - Hypothesis Testing.ipynb" \
  --output output/"04_Hypothesis_Testing_out.ipynb"

jupyter nbconvert \
  --to notebook --execute notebooks/"05_Model_Training_and_Evaluation.ipynb" \
  --output output/"05_Model_Training_out.ipynb"

echo "✅ All notebooks complete. Launching app…"

exec streamlit run app.py
