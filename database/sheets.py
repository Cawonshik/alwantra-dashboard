import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from database.config import SPREADSHEET_NAME

# ================= AUTH =================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def get_client():
    creds_json = os.environ.get("GOOGLE_SHEETS_CREDS_JSON")

    if not creds_json:
        raise Exception("GOOGLE_SHEETS_CREDS_JSON not found")

    creds_dict = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    return gspread.authorize(creds)


# ================= GET SPREADSHEET =================

def get_spreadsheet():
    client = get_client()
    try:
        return client.open(SPREADSHEET_NAME)
    except:
        return client.create(SPREADSHEET_NAME)


# ================= GET SHEET =================

def get_sheet(sheet_name):
    sh = get_spreadsheet()
    try:
        return sh.worksheet(sheet_name)
    except:
        return sh.add_worksheet(title=sheet_name, rows="2000", cols="20")


# ================= INIT SHEET =================

def init_sheet(sheet_name, headers):
    sheet = get_sheet(sheet_name)

    existing = sheet.get_all_values()

    if not existing:
        sheet.append_row(headers)