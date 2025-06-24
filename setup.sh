#!/usr/bin/env bash
set -e

# ── 1) Streamlit config ────────────────────────────────────────────────────────
mkdir -p ~/.streamlit/
cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
port = $PORT
enableCORS = false
EOF

echo "📝 Running notebooks to generate data and model…"
jupyter nbconvert --to notebook --execute notebooks/01_clean_data.ipynb \
  --output output/01_clean_data_out.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_train_model.ipynb \
  --output output/02_train_model_out.ipynb

# (add more notebooks as needed)

echo "✅ Notebooks done."

# ── 3) Launch Streamlit ────────────────────────────────────────────────────────
exec streamlit run app.py