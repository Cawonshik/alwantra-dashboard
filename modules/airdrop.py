import uuid
from datetime import datetime
from functools import lru_cache

from database.sheets import get_sheet
from database.config import SHEET_AIRDROP


# ================= INTERNAL CACHE =================

@lru_cache(maxsize=1)
def _get_all_cached():

    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_values()

    if not rows:
        return []

    data = []

    for r in rows[1:]:

        if not r:
            continue

        # Pastikan panjang kolom cukup
        r = r + [""] * (10 - len(r))

        data.append({
            "id": r[0],
            "user_id": r[1],
            "name": r[2],
            "type": r[3],
            "chain": r[4],
            "wallet": r[5],
            "channel": r[6],
            "note": r[7],
            "status": r[8],
            "date": r[9],
        })

    return data


# ================= GET ALL =================

def get_all(user_id):

    data = _get_all_cached()

    return [
        r for r in data
        if str(r["user_id"]) == str(user_id)
    ]


# ================= GET BY ID =================

def get_by_id(id, user_id):

    data = _get_all_cached()

    for r in data:

        if (
            str(r["id"]) == str(id)
            and str(r["user_id"]) == str(user_id)
        ):
            return r

    return None


# ================= ADD =================

def add(data, user_id):

    sheet = get_sheet(SHEET_AIRDROP)

    sheet.append_row([

        str(uuid.uuid4()),                     # id
        user_id,                               # user_id
        data.get("name", ""),                  # name
        data.get("type", ""),                  # type
        data.get("chain", ""),                 # chain
        data.get("wallet", ""),                # wallet
        data.get("channel", ""),               # channel
        data.get("note", ""),                  # note
        "pending",                             # status
        datetime.now().strftime("%Y-%m-%d")    # date

    ])

    _get_all_cached.cache_clear()


# ================= DELETE =================

def delete(id, user_id):

    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(id)
            and str(r[1]) == str(user_id)
        ):

            sheet.delete_rows(i)
            break

    _get_all_cached.cache_clear()


# ================= DONE =================

def done(id, user_id):

    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(id)
            and str(r[1]) == str(user_id)
        ):

            sheet.update_cell(i, 9, "done")
            break

    _get_all_cached.cache_clear()


# ================= UPDATE =================

def update(id, data, user_id):

    sheet = get_sheet(SHEET_AIRDROP)
    rows = sheet.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(id)
            and str(r[1]) == str(user_id)
        ):

            sheet.update(
                f"C{i}:H{i}",
                [[
                    data.get("name", ""),
                    data.get("type", ""),
                    data.get("chain", ""),
                    data.get("wallet", ""),
                    data.get("channel", ""),
                    data.get("note", "")
                ]]
            )

            break

    _get_all_cached.cache_clear()