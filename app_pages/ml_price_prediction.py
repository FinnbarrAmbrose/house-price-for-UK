import streamlit as st
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

def ml_price_prediction_body():
    st.title("🤖 Machine Learning Model")
    st.write("Train/test metrics, residuals & feature importances for the regression model.")

    model_path = "outputs/models/house_price_pipeline.pkl"
    try:
        pipeline = joblib.load(model_path)
    except FileNotFoundError:
        st.error(f"Pipeline not found at {model_path!r}. Run Notebook 05 first.")
        return

    df = pd.read_csv("outputs/datasets/collection/HousePricesRecords_clean.csv")
    X = df.drop(columns=["Price", "Date of Transfer"], errors="ignore")
    y = df["Price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )

    y_train_pred = pipeline.predict(X_train)
    y_test_pred  = pipeline.predict(X_test)

    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae  = mean_absolute_error(y_test,  y_test_pred)
    train_r2  = r2_score(y_train,   y_train_pred)
    test_r2   = r2_score(y_test,    y_test_pred)

    st.subheader("Model Performance")
    st.metric("Train MAE", f"£{train_mae:,.0f}")
    st.metric("Test MAE",  f"£{test_mae:,.0f}")
    st.metric("Train R²",  f"{train_r2:.2f}")
    st.metric("Test R²",   f"{test_r2:.2f}")

    ohe = pipeline.named_steps["preprocessor"].named_transformers_["cat"]
    cat_cols = ohe.get_feature_names_out(
        pipeline.named_steps["preprocessor"].transformers_[1][2]
    )
    feat_names = list(pipeline.named_steps["preprocessor"].transformers_[0][2]) + list(cat_cols)
    importances = pipeline.named_steps["regressor"].feature_importances_
    idx_sorted  = np.argsort(importances)[-10:]

    fig, ax = plt.subplots()
    ax.barh(np.array(feat_names)[idx_sorted], importances[idx_sorted])
    ax.set_title("Top 10 Feature Importances")
    st.pyplot(fig)