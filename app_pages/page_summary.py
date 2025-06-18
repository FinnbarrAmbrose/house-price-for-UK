import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ── Load dynamic metrics (produced by Notebook 05) ───────────────────────────
METRICS_FILE = Path("outputs/models/metrics.json")
if METRICS_FILE.exists():
    with open(METRICS_FILE, "r") as f:
        m = json.load(f)
    MODEL_MAE   = m.get("mae", None)
    MODEL_RMSE  = m.get("rmse", None)
    MODEL_R2    = m.get("r2",   None)
else:
    MODEL_MAE   = MODEL_RMSE = MODEL_R2 = None

def page_summary_body() -> None:
    """Landing page – project overview & quick dataset glimpse."""
    st.title("🏠 UK House-Price Estimator – Overview")

    st.markdown(
        """
        This dashboard lets UK house-hunters and data enthusiasts  
        explore historic **Price-Paid** transactions, test a few
        market hypotheses, and obtain an instant sale-price prediction.
        """
    )

    # ── Dataset snapshot ───────────────────────────────────────────────────────
    st.subheader("↘️ Data snapshot")
    data_path = Path("outputs/datasets/collection/HousePricesRecords_clean.csv")

    if data_path.exists():
        df = pd.read_csv(data_path)
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"Dataset dimensions: **{df.shape[0]:,} rows × {df.shape[1]} columns**")
    else:
        st.warning("Cleaned CSV not found – run Notebook 02 to generate it.")

    # ── KPI metrics ────────────────────────────────────────────────────────────
    st.subheader("⚙️ Latest model metrics")

    col1, col2, col3 = st.columns(3)

    if MODEL_MAE is not None:
        col1.metric("MAE (Mean Absolute Error)",    f"£{MODEL_MAE:,.0f}")
        col2.metric("RMSE (Root Mean Squared Error)", f"£{MODEL_RMSE:,.0f}")
        col3.metric("R² (Coefficient of Determination)", f"{MODEL_R2:.2f}")
    else:
        col1.metric("MAE",  "n/a")
        col2.metric("RMSE", "n/a")
        col3.metric("R²",   "n/a")
        st.info("Metrics will appear here after you run Notebook 05 and regenerate `metrics.json`.")

    st.markdown(
        """
        Metrics are loaded live from `outputs/models/metrics.json`.  
        To refresh them, re-run *Notebook 05_Model_Training_and_Evaluation*.
        
        **Metric definitions:**  
        - **MAE**: On average, how many pounds you’re off by (lower is better).  
        - **RMSE**: Similar to MAE but penalises big misses more heavily.  
        - **R²**: Percentage of the price-variance your model “captures” (1.00 is perfect).
        """)
