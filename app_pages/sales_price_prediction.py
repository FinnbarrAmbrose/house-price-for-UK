import streamlit as st
import pandas as pd
import joblib
import os

def sales_price_prediction_body():
    st.title("🔮 Sale Price Prediction")
    st.write("Enter property details below and click **Predict Price** to get an estimated sale price.")

    # 1) Load data for dropdowns
    data_path = "outputs/datasets/collection/HousePricesRecords_clean.csv"
    df = pd.read_csv(data_path)
    df["Date of Transfer"] = pd.to_datetime(df["Date of Transfer"])
    max_date = df["Date of Transfer"].max()
    min_date = max_date - pd.DateOffset(years=3)

    # 2) Load pipeline
    model_path = "outputs/models/house_price_pipeline.pkl"
    if not os.path.exists(model_path):
        st.error(f"Pipeline not found at {model_path!r}. Run Notebook 05 first.")
        return
    pipeline = joblib.load(model_path)

    # 3) PPD mapping
    ppd_map = {
        "A": "Standard sale (market value)",
        "B": "Other sale types (repossessions, buy-to-let, etc.)"
    }
    reverse_ppd = {v: k for k, v in ppd_map.items()}

    # 4) Build the form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Date picker (last 3 years)
            transfer_date = st.date_input(
                "Date of Transfer",
                value=max_date.date(),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
            year  = transfer_date.year
            month = transfer_date.month

            ppd_label    = st.selectbox("Sale Category", list(ppd_map.values()))
            ppd_category = reverse_ppd[ppd_label]

            old_new_label = st.radio("Is this a new build?", ("No", "Yes"))
            old_new       = 1 if old_new_label == "Yes" else 0

        with col2:
            tenure_label = st.radio("Tenure", ("Leasehold", "Freehold"))
            tenure       = 1 if tenure_label == "Freehold" else 0

            region   = st.selectbox("Town/City", sorted(df["Town/City"].unique()))
            county   = st.selectbox("County", sorted(df["County"].unique()))
            prop_type = st.selectbox(
                "Property Type",
                ["Detached", "Flat", "Semi-Detached", "Terraced"]
            )

        # **Submit button inside form**
        submitted = st.form_submit_button("Predict Price")

    # 5) Only run prediction if the form was submitted
    if submitted:
        # Compute aggregates
        region_median = df[df["Town/City"] == region]["Price"].median()
        region_count  = int(df["Town/City"].value_counts()[region])
        county_median = df[df["County"]    == county]["Price"].median()
        county_count  = int(df["County"].value_counts()[county])

        # Build input_df with all required columns
        input_df = pd.DataFrame([{
            "Year":                year,
            "Month":               month,
            "PPDCategory Type":    ppd_category,
            "Old/New":             old_new,
            "Duration":            tenure,
            "Town/City":           region,
            "County":              county,
            "Property_D":          1 if prop_type == "Detached"      else 0,
            "Property_F":          1 if prop_type == "Flat"          else 0,
            "Property_S":          1 if prop_type == "Semi-Detached" else 0,
            "Property_T":          1 if prop_type == "Terraced"      else 0,
            "Region":              region,
            "RegionMedianPrice":   region_median,
            "RegionSaleCount":     region_count,
            "CountyMedianPrice":   county_median,
            "CountySaleCount":     county_count,
        }])

        # Predict and display
        price_pred = pipeline.predict(input_df)[0]
        st.success(f"🏠 Estimated Sale Price: **£{price_pred:,.0f}**")
