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

# ── 2) Execute your notebooks ───────────────────────────────────────────────────
echo "📝 Executing notebooks via nbconvert…"
jupyter nbconvert \
  --to notebook \
  --execute notebooks/clean_data.ipynb \
  --output output/clean_data_out.ipynb

jupyter nbconvert \
  --to notebook \
  --execute notebooks/train_model.ipynb \
  --output output/train_model_out.ipynb

# (add more notebooks as needed)

echo "✅ Notebooks done."

# ── 3) Launch Streamlit ────────────────────────────────────────────────────────
exec streamlit run app.py