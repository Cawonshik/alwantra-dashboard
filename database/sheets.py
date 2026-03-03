import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from database.config import SPREADSHEET_NAME

# ================= AUTH =================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)


# ================= GET SPREADSHEET =================

def get_spreadsheet():
    try:
        return client.open(SPREADSHEET_NAME)
    except:
        # kalau belum ada → create otomatis
        sh = client.create(SPREADSHEET_NAME)
        return sh


# ================= GET SHEET =================

def get_sheet(sheet_name):
    sh = get_spreadsheet()
    try:
        return sh.worksheet(sheet_name)
    except:
        # kalau sheet belum ada → create kosong
        return sh.add_worksheet(title=sheet_name, rows="2000", cols="20")


# ================= INIT SHEET =================

def init_sheet(sheet_name, headers):
    sheet = get_sheet(sheet_name)

    existing = sheet.get_all_values()

    # kalau kosong → set header
    if not existing:
        sheet.append_row(headers)