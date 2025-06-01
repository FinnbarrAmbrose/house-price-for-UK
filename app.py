import streamlit as st
import pandas as pd
import joblib
import os

# Load model and expected feature order
model, feature_order = joblib.load("outputs/models/house_price_model.pkl")

st.title("🏠 UK House Price Estimator")
st.write("Fill in the details to predict the estimated sale price.")

# User Inputs
year = st.number_input("Year of Sale", min_value=1995, max_value=2025, value=2020)
month = st.selectbox("Month of Sale", list(range(1, 13)))
old_new = st.selectbox("Property Age", ["Old", "New"])
duration = st.selectbox("Ownership Type", ["Freehold", "Leasehold"])
property_type = st.selectbox("Property Type", ["Detached", "Semi-detached", "Flats/Maisonettes", "Terraced"])

# Prepare input for prediction
input_data = {
    "Year": year,
    "Month": month,
    "Old/New": 1 if old_new == "New" else 0,
    "Duration": 1 if duration == "Freehold" else 0,
    "Property_D": 1 if property_type == "Detached" else 0,
    "Property_S": 1 if property_type == "Semi-detached" else 0,
    "Property_F": 1 if property_type == "Flats/Maisonettes" else 0,
    "Property_T": 1 if property_type == "Terraced" else 0,
}

# Reorder input to match training
input_df = pd.DataFrame([input_data])
input_df = input_df[feature_order]

# Predict
prediction = model.predict(input_df)[0]

# Show result
st.subheader("Estimated Sale Price:")
st.write(f"£{prediction:,.2f}")
