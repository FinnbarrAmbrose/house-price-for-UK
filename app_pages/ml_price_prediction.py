# app_pages/ml_price_prediction.py

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import plotly.express as px
import numpy as np

# Paths
DATA_PATH   = Path("outputs/datasets/collection/HousePricesRecords_clean.csv")
MODEL_PATH  = Path("outputs/models/house_price_model.pkl")
COLS_PATH   = Path("outputs/models/model_columns.pkl")

def ml_price_prediction_body():
    st.title("🤖 Machine Learning Model")
    st.markdown("Train/test metrics, residuals & feature importances for the regression model.")

    # --- Load data & model ---
    if not DATA_PATH.exists():
        st.error("Cleaned data not found. Please run notebook 01 first.")
        return
    if not MODEL_PATH.exists() or not COLS_PATH.exists():
        st.error("Model or columns file missing. Run notebook 05 to generate them.")
        return

    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    model_cols = joblib.load(COLS_PATH)

    # --- Prepare features/target ---
    y = df["Price"]
    X = df.drop(columns=["Price", "Date of Transfer"], errors="ignore")
    X = pd.get_dummies(X, drop_first=True)

    # ensure full column set
    for c in model_cols:
        if c not in X.columns:
            X[c] = 0
    X = X[model_cols]

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )

    # --- Compute metrics ---
    def metrics(y_true, y_pred):
        return {
            "R²": r2_score(y_true, y_pred),
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": mean_squared_error(y_true, y_pred, squared=False),
        }

    y_pred_train = model.predict(X_train)
    y_pred_test  = model.predict(X_test)

    m_train = metrics(y_train, y_pred_train)
    m_test  = metrics(y_test, y_pred_test)

    # --- Display metrics ---
    st.subheader("🔧 Metrics")
    cols = st.columns(3)
    cols[0].metric("R² (train)", f"{m_train['R²']:.2f}", delta=f"{m_test['R²']-m_train['R²']:+.2f}")
    cols[1].metric("MAE (train)", f"£{m_train['MAE']:,.0f}", delta=f"£{m_test['MAE']-m_train['MAE']:,.0f}")
    cols[2].metric("RMSE (train)", f"£{m_train['RMSE']:,.0f}", delta=f"£{m_test['RMSE']-m_train['RMSE']:,.0f}")

    st.caption("Delta shows (test – train) change.")

    # --- Actual vs Predicted scatter ---
    st.subheader("📈 Actual vs Predicted Prices (test set)")
    fig1 = px.scatter(
        x=y_test, y=y_pred_test,
        labels={"x":"Actual Sale Price", "y":"Predicted Sale Price"},
        title="Actual vs Predicted"
    )
    fig1.add_shape(  # perfect prediction line
        type="line", line=dict(dash="dash"),
        x0=y_test.min(), x1=y_test.max(),
        y0=y_test.min(), y1=y_test.max()
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Feature importance ---
    st.subheader("🏅 Top 10 Feature Importances (coefficients)")
    coefs = pd.Series(model.coef_, index=model_cols)
    top10 = coefs.abs().sort_values(ascending=False).head(10).index
    fig2 = px.bar(
        x=coefs.loc[top10],
        y=top10,
        orientation="h",
        labels={"x":"Coefficient", "y":""},
        title="Top 10 Most Influential Features"
    )
    fig2.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig2, use_container_width=True)
