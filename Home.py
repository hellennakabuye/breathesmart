import streamlit as st
from utils import authenticate_user

st.set_page_config(page_title="BreatheSmart UG", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None

st.image("breathesmartug.png", width=220)
st.title("BreatheSmart UG")
st.subheader("Secure NGO Login")

if not st.session_state.authenticated:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        success, role = authenticate_user(username, password)

        if success:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    st.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()
