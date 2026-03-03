import uuid
from datetime import datetime
from database.sheets import get_sheet
from database.config import SHEET_AIRDROP

# ================= GET ALL =================
def get_all(user_id):
    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_records()
    return [r for r in rows if r["user_id"] == user_id]


# ================= ADD =================
def add(data, user_id):
    sheet = get_sheet(SHEET_AIRDROP)

    sheet.append_row([
        str(uuid.uuid4()),
        user_id,
        data.get("name",""),
        data.get("type",""),
        data.get("chain",""),
        data.get("wallet",""),
        data.get("channel",""),
        data.get("note",""),
        "pending",
        datetime.now().strftime("%Y-%m-%d")
    ])


# ================= DELETE =================
def delete(id, user_id):
    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_records()

    for i, r in enumerate(rows, start=2):
        if r["id"] == id and r["user_id"] == user_id:
            sheet.delete_rows(i)
            break


# ================= DONE =================
def done(id, user_id):
    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_records()

    for i, r in enumerate(rows, start=2):
        if r["id"] == id and r["user_id"] == user_id:
            sheet.update_cell(i, 9, "done")  # kolom status
            break


# ================= UPDATE =================
def update(id, data, user_id):
    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_records()

    for i, r in enumerate(rows, start=2):
        if r["id"] == id and r["user_id"] == user_id:
            sheet.update(f"C{i}:H{i}", [[
                data.get("name",""),
                data.get("type",""),
                data.get("chain",""),
                data.get("wallet",""),
                data.get("channel",""),
                data.get("note","")
            ]])
            break