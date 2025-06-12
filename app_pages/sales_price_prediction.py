# app_pages/sales_price_prediction.py

import streamlit as st
import pandas as pd
import joblib

def sales_price_prediction_body():
    st.title("🔮 Sale Price Prediction")
    st.markdown("Use this tool to predict the estimated sale price of a UK property.")

    # --- Load model and column list ---
    try:
        model = joblib.load("outputs/models/house_price_model.pkl")
        model_columns = joblib.load("outputs/models/model_columns.pkl")
    except FileNotFoundError:
        st.warning("Model files not found. Ensure 'house_price_model.pkl' and 'model_columns.pkl' exist.")
        return

    # --- User Input Form ---
    st.header("🏠 Enter Property Details:")

    col1, col2 = st.columns(2)
    with col1:
        year = st.slider("Year of Sale", 1995, 2024, 2020)
        month = st.selectbox("Month of Sale", list(range(1, 13)))
        old_new = st.selectbox("Property Age", ["Old", "New"])
    with col2:
        duration = st.selectbox("Tenure", ["Freehold", "Leasehold"])
        property_type = st.selectbox("Property Type", ["Detached", "Flat", "Semi", "Terraced"])

    if st.button("💰 Predict Price"):
        # Build one-row DataFrame from inputs
        input_dict = {
            "Year": year,
            "Month": month,
            "Old/New": 1 if old_new == "New" else 0,
            "Duration": 1 if duration == "Freehold" else 0,
            "Property_D": property_type == "Detached",
            "Property_F": property_type == "Flat",
            "Property_S": property_type == "Semi",
            "Property_T": property_type == "Terraced"
        }

        input_df = pd.DataFrame([input_dict])

        # Ensure all model columns are present
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[model_columns]  # match model column order

        # Predict
        prediction = model.predict(input_df)[0]
        st.success(f"🏷️ Predicted Sale Price: £{prediction:,.0f}")
        st.caption("Note: Estimate is based on historical UK Land Registry data.")