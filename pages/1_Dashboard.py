import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must login to access this page.")
    st.stop()

st.set_page_config(layout="wide")

st.image("breathesmartug.png", width=320)

st.title("📊 NGO Admin Dashboard")

df = load_data()

# Sidebar Filters
division = st.sidebar.selectbox(
    "Select Division",
    ["All"] + sorted(df["Division"].unique().tolist())
)

if division != "All":
    df = df[df["Division"] == division]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Screenings", len(df))

with col2:
    st.metric("High Risk Cases", df[df["Risk"] == "High"].shape[0])

with col3:
    st.metric("Moderate Risk", df[df["Risk"] == "Moderate"].shape[0])

with col4:
    st.metric("Divisions Covered", df["Division"].nunique())

st.markdown("---")

# Risk Trend Chart
st.subheader("Monthly Respiratory Risk Trends")

df["Date"] = pd.to_datetime(df["Date"])
monthly = df.groupby(pd.Grouper(key="Date", freq="M")).size().reset_index(name="Cases")

chart = alt.Chart(monthly).mark_line().encode(
    x="Date:T",
    y="Cases:Q"
).properties(height=400)

st.altair_chart(chart, use_container_width=True)
