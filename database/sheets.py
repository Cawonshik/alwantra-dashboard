import os
import json
import gspread

from functools import lru_cache
from oauth2client.service_account import ServiceAccountCredentials
from database.config import SPREADSHEET_NAME


# ================= AUTH SCOPE =================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


# ==================================================
# GET GOOGLE CLIENT (CACHED)
# ==================================================

@lru_cache(maxsize=1)
def get_client():

    creds_json = os.environ.get("GOOGLE_SHEETS_CREDS_JSON")

    # ===== ENV VARIABLE (Vercel / Railway) =====
    if creds_json:

        creds_dict = json.loads(creds_json)

    # ===== LOCAL FILE =====
    elif os.path.exists("credentials.json"):

        with open("credentials.json") as f:
            creds_dict = json.load(f)

    else:

        raise Exception("Google credentials not found")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    return gspread.authorize(creds)


# ==================================================
# GET SPREADSHEET (CACHED)
# ==================================================

@lru_cache(maxsize=1)
def get_spreadsheet():

    client = get_client()

    try:

        return client.open(SPREADSHEET_NAME)

    except Exception:

        return client.create(SPREADSHEET_NAME)


# ==================================================
# GET SHEET
# ==================================================

def get_sheet(sheet_name):

    sh = get_spreadsheet()

    try:

        return sh.worksheet(sheet_name)

    except Exception:

        return sh.add_worksheet(
            title=sheet_name,
            rows="2000",
            cols="20"
        )


# ==================================================
# INIT SHEET
# ==================================================

def init_sheet(sheet_name, headers):

    sheet = get_sheet(sheet_name)

    existing = sheet.get_all_values()

    if not existing:

        sheet.append_row(headers)