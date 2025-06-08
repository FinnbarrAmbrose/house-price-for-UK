import streamlit as st

from app_pages.multipage import MultiPage
from app_pages.page_summary import page_summary_body
from app_pages.correlation_analysis import correlation_analysis_body
from app_pages.sales_price_prediction import sales_price_prediction_body
from app_pages.project_hypothesis import project_hypothesis_body
from app_pages.ml_price_prediction import ml_price_prediction_body

app = MultiPage(app_name="Property-Value-Maximizer")

app.add_page("👁️ Project Overview",     page_summary_body)
app.add_page("📈 Correlation Analysis",  correlation_analysis_body)
app.add_page("🔮 Sale Price Prediction", sales_price_prediction_body)
app.add_page("🔬 Hypothesis Validation", project_hypothesis_body)
app.add_page("🤖 Machine Learning Model", ml_price_prediction_body)

app.run()
