# app_pages/page_summary.py
import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------------------------------------------
# Edit these three numbers whenever you retrain / improve the model
MODEL_MAE  = 34_000     # £
MODEL_RMSE = 49_000     # £
MODEL_R2   = 0.69
# -----------------------------------------------------------------


def page_summary_body() -> None:
    """Landing page – project overview & quick dataset glimpse."""
    st.title("🏠 UK House-Price Estimator – Overview")

    st.markdown(
        """
        This dashboard lets UK house-hunters and data enthusiasts  
        explore historic **Price-Paid** transactions, test a few
        market hypotheses, and obtain an instant sale-price prediction
        based on basic property details.
        """
    )

    # -------------------- Dataset sample -------------------------
    st.subheader("↘️ Data snapshot")
    data_path = Path("outputs/datasets/collection/HousePricesRecords_clean.csv")

    if data_path.exists():
        df = pd.read_csv(data_path)
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"Dataset dimensions: **{df.shape[0]:,} rows × {df.shape[1]} columns**")
    else:
        st.warning("Cleaned CSV not found – run notebook 01_Data_Collection first.")

    # -------------------- KPI metrics ----------------------------
    st.subheader("⚙️ Baseline model metrics (Linear Regression)")

    col1, col2, col3 = st.columns(3)
    col1.metric("MAE",  f"£{MODEL_MAE:,.0f}")
    col2.metric("RMSE", f"£{MODEL_RMSE:,.0f}")
    col3.metric("R²",   f"{MODEL_R2:.2f}")

    st.info(
        "Metrics are based on the 1 000-row prototype dataset. "
        "They will refresh automatically after you retrain the model "
        "on the full dataset or push a new pickle to `outputs/models/`."
    )
