import uuid
from database.sheets import get_sheet
from database.config import SHEET_AKUN


# ================= GET ALL =================
def get_all(user_id):
    sheet = get_sheet(SHEET_AKUN)
    rows = sheet.get_all_records()

    return [
        r for r in rows
        if str(r["user_id"]) == str(user_id)
    ]


# ================= GET BY ID =================
def get_by_id(id, user_id):
    sheet = get_sheet(SHEET_AKUN)
    rows = sheet.get_all_records()

    for r in rows:
        if str(r["id"]) == str(id) and str(r["user_id"]) == str(user_id):
            return r

    return None


# ================= ADD =================
def add(data, user_id):
    sheet = get_sheet(SHEET_AKUN)

    sheet.append_row([
        str(uuid.uuid4()),   # ID unik
        user_id,
        data.get("gmail", ""),
        data.get("twitter", ""),
        data.get("telegram", ""),
        data.get("discord", ""),
        data.get("github", "")
    ])


# ================= DELETE =================
def delete(id, user_id):
    sheet = get_sheet(SHEET_AKUN)
    rows = sheet.get_all_records()

    for i, r in enumerate(rows, start=2):
        if str(r["id"]) == str(id) and str(r["user_id"]) == str(user_id):
            sheet.delete_rows(i)
            break


# ================= UPDATE =================
def update(id, data, user_id):
    sheet = get_sheet(SHEET_AKUN)
    rows = sheet.get_all_records()

    for i, r in enumerate(rows, start=2):
        if str(r["id"]) == str(id) and str(r["user_id"]) == str(user_id):
            sheet.update(f"C{i}:G{i}", [[
                data.get("gmail", ""),
                data.get("twitter", ""),
                data.get("telegram", ""),
                data.get("discord", ""),
                data.get("github", "")
            ]])
            break