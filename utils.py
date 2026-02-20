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

def load_data():
    client = get_client()
    sheet = client.open("BreatheSmart_Data").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def authenticate_user(username, password):
    client = get_client()
    sheet = client.open("Admin_Users").sheet1
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
