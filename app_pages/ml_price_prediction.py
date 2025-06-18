import streamlit as st
import pandas as pd
import joblib
import json
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

def ml_price_prediction_body():
    st.title("🤖 Machine Learning Model")
    st.write("Train/test metrics, residuals & feature importances for the regression model.")

    # ── 1) Load trained pipeline ────────────────────────────────────────────────
    pipeline_path = Path("outputs/models/house_price_pipeline.pkl")
    if not pipeline_path.exists():
        st.error(f"Pipeline not found at {pipeline_path!r}. Run Notebook 05 first.")
        return
    pipeline = joblib.load(pipeline_path)

    # ── 2) Load or compute test‐set metrics ────────────────────────────────────
    metrics_path = Path("outputs/models/metrics.json")
    if metrics_path.exists():
        with open(metrics_path, "r") as f:
            m = json.load(f)
        test_mae  = m.get("mae", None)
        test_rmse = m.get("rmse", None)
        test_r2   = m.get("r2",   None)
    else:
        test_mae = test_rmse = test_r2 = None

    # ── 3) Reload data & split for train‐set metrics ──────────────────────────
    df = pd.read_csv("outputs/datasets/collection/HousePricesRecords_clean.csv")
    X  = df.drop(columns=["Price", "Date of Transfer"], errors="ignore")
    y  = df["Price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )

    # ── 4) Predict & compute train‐set metrics ────────────────────────────────
    y_train_pred = pipeline.predict(X_train)
    train_mae    = mean_absolute_error(y_train, y_train_pred)
    train_rmse   = mean_squared_error(y_train, y_train_pred, squared=False)
    train_r2     = r2_score(y_train, y_train_pred)

    # ── 5) Display metrics with tooltips ───────────────────────────────────────
    st.subheader("Model Performance")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric(
        label="Train MAE (Mean Absolute Error)",
        value=f"£{train_mae:,.0f}",
        help="Average absolute difference between predicted & actual prices on the training set"
    )
    c2.metric(
        label="Train RMSE (Root Mean Squared Error)",
        value=f"£{train_rmse:,.0f}",
        help="Root of mean squared errors; penalises larger mistakes on the training set"
    )
    c3.metric(
        label="Train R² (Coefficient of Determination)",
        value=f"{train_r2:.2f}",
        help="Portion of price variance explained by the model on the training set"
    )

    if test_mae is not None:
        c4.metric(
            label="Test MAE",
            value=f"£{test_mae:,.0f}",
            help="Average absolute error on the hold-out test set"
        )
        c5.metric(
            label="Test RMSE",
            value=f"£{test_rmse:,.0f}",
            help="Root mean squared error on the hold-out test set"
        )
        c6.metric(
            label="Test R²",
            value=f"{test_r2:.2f}",
            help="R² on the hold-out test set"
        )
    else:
        c4.metric("Test MAE", "n/a")
        c5.metric("Test RMSE", "n/a")
        c6.metric("Test R²", "n/a")
        st.info("Run Notebook 05 to regenerate `metrics.json` before these appear.")

    # ── 6) Feature importances ────────────────────────────────────────────────
    st.subheader("Feature Importances (Top 10)")

    ohe = pipeline.named_steps["preprocessor"].named_transformers_["cat"]
    cat_cols = ohe.get_feature_names_out(
        pipeline.named_steps["preprocessor"].transformers_[1][2]
    )
    num_cols = list(pipeline.named_steps["preprocessor"].transformers_[0][2])
    feature_names = num_cols + list(cat_cols)

    importances = pipeline.named_steps["regressor"].feature_importances_
    idx_sorted  = np.argsort(importances)[-10:]

    fig, ax = plt.subplots()
    ax.barh(np.array(feature_names)[idx_sorted], importances[idx_sorted])
    ax.set_title("Top 10 Feature Importances")
    st.pyplot(fig)
