import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must login to access this page.")
    st.stop()

st.set_page_config(layout="wide")

st.image("breathesmartug.png", width=320)

st.title("🗺 Division Risk Heatmap")

df = load_data()

division_counts = df.groupby(["Division", "Risk"]).size().reset_index(name="Cases")

heatmap_data = division_counts.pivot(
    index="Division",
    columns="Risk",
    values="Cases"
).fillna(0)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("18% increase in risk alerts during dust season.")
