# app_pages/correlation_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path
import numpy as np

DATA_PATH = Path("outputs/datasets/collection/HousePricesRecords_clean.csv")


def correlation_analysis_body() -> None:
    """EDA tab – distribution & correlation plots."""
    st.title("📊 Correlation Analysis")

    # -----------------------------------------------------------
    # 1 · Load data
    # -----------------------------------------------------------
    if not DATA_PATH.exists():
        st.error("Cleaned dataset not found. Run notebook 01 to generate it.")
        return

    df = pd.read_csv(DATA_PATH)

    # -----------------------------------------------------------
    # 2 · Sidebar filters
    # -----------------------------------------------------------
    st.sidebar.header("Filter data ⬇️")

    years = sorted(df["Year"].unique())
    counties = sorted(df["County"].unique())

    year_sel = st.sidebar.multiselect("Year", years, default=years)
    county_sel = st.sidebar.multiselect("County", counties, default=counties[:10])

    df_filt = df.query("Year in @year_sel and County in @county_sel")

    st.write(f"Filtered dataset: **{df_filt.shape[0]:,} rows**")

    # -----------------------------------------------------------
    # 3 · Price distribution (hist + KDE)
    # -----------------------------------------------------------
    st.subheader("💷 Price distribution")

    hist_fig = px.histogram(
        df_filt,
        x="Price",
        nbins=50,
        marginal="box",
        title="Sale-price histogram (interactive)",
        template="plotly_white",
    )
    hist_fig.update_layout(yaxis_title="Count")
    st.plotly_chart(hist_fig, use_container_width=True)

    # -----------------------------------------------------------
    # 4 · Correlation heat-map (toggle pearson / spearman)
    # -----------------------------------------------------------
    st.subheader("🔗 Numeric correlations")

    method = st.radio(
        "Correlation method",
        ["pearson", "spearman"],
        horizontal=True,
    )
    corr = df_filt.select_dtypes(np.number).corr(method=method)
    corr_values = corr.values

    heat_fig = ff.create_annotated_heatmap(
        z=corr_values,
        x=list(corr.columns),
        y=list(corr.index),
        colorscale="RdBu",
        showscale=True,
        zmin=-1,
        zmax=1,
        annotation_text=np.round(corr_values, 2),
    )
    heat_fig.update_layout(height=600, template="plotly_white")
    st.plotly_chart(heat_fig, use_container_width=True)

    st.caption(
        "Positive values indicate direct correlation, negative values inverse. "
        "Hover any cell for exact coefficient."
    )
