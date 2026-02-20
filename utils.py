import pandas as pd
import gspread
import bcrypt
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scope
    )
    return gspread.authorize(creds)

import pandas as pd
import gspread
import bcrypt
import streamlit as st
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def load_data():
    client = get_client()
    spreadsheet = client.open("BreatheSmart_Data")
    sheet = spreadsheet.worksheet("logs")

    data = sheet.get_all_records()
    return pd.DataFrame(data)

def authenticate_user(username, password):
    client = get_client()

    # Open main spreadsheet
    spreadsheet = client.open("BreatheSmart_Data")

    # Open Admin_Users worksheet inside it
    sheet = spreadsheet.worksheet("Admin_Users")

    users = pd.DataFrame(sheet.get_all_records())

    users.columns = users.columns.str.strip()

    user = users[users["Username"] == username]

    if user.empty:
        return False, None

    stored_hash = user.iloc[0]["Password"]
    role = user.iloc[0]["Role"]

    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return True, role

    return False, None
