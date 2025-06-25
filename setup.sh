#!/usr/bin/env bash
set -euo pipefail

echo "📝 Running all notebooks…"

# 1) ensure writable folders exist under /app
mkdir -p outputs/datasets/collection outputs/models

# 2) execute each notebook in place, writing outputs back to /app/outputs
pushd jupyter_notebooks > /dev/null

NOTEBOOKS=(
  "01 - Data Collection-1.ipynb"
  "02_data_cleaning (1).ipynb"
  "03 - Exploratory Data Analysis.ipynb"
  "04 - Hypothesis Testing.ipynb"
  "05_Model_Training_and_Evaluation.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
  echo "⏳ Executing $nb"
  jupyter nbconvert \
    --to notebook \
    --execute "$nb" \
    --output "../outputs/${nb%.*}_out.ipynb" \
    --ExecutePreprocessor.timeout=600
done

popd > /dev/null

echo "✅ All notebooks complete. Launching Streamlit…"
exec streamlit run app.py --server.port="$PORT"
