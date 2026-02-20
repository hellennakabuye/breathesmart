import streamlit as st
from utils import load_data
from datetime import datetime


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must login to access this page.")
    st.stop()
st.set_page_config(layout="wide")

st.title("📄 Monthly Impact Report")

df = load_data()

month = datetime.now().strftime("%B %Y")

st.markdown(f"## BreatheSmart UG Report – {month}")

total = len(df)
high = df[df["Risk"] == "High"].shape[0]
moderate = df[df["Risk"] == "Moderate"].shape[0]

st.write(f"Total Screenings: {total}")
st.write(f"High Risk Cases: {high}")
st.write(f"Moderate Risk Cases: {moderate}")

if st.button("📥 Download PDF Report"):
    st.success("PDF generation logic can be inserted here.")

