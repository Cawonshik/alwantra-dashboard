import uuid
from functools import lru_cache
from database.sheets import get_sheet
from database.config import SHEET_AKUN


# ================= INTERNAL CACHE =================

@lru_cache(maxsize=1)
def _get_all_cached():

    sheet = get_sheet(SHEET_AKUN)

    rows = sheet.get_all_records()

    if not rows:
        return []

    data = []

    for r in rows:

        data.append({

            "id": str(r.get("id", "")).strip(),
            "user_id": str(r.get("user_id", "")).strip(),

            "gmail": str(r.get("gmail", "")).strip(),
            "twitter": str(r.get("twitter", "")).strip(),
            "telegram": str(r.get("telegram", "")).strip(),
            "discord": str(r.get("discord", "")).strip(),
            "github": str(r.get("github", "")).strip(),

        })

    return data


# ================= GET ALL =================

def get_all(user_id):

    data = _get_all_cached()

    return [
        r for r in data
        if str(r.get("user_id")) == str(user_id)
    ]


# ================= GET BY ID =================

def get_by_id(id, user_id):

    data = _get_all_cached()

    for r in data:

        if (
            str(r.get("id")) == str(id)
            and str(r.get("user_id")) == str(user_id)
        ):
            return r

    return None


# ================= ADD =================

def add(data, user_id):

    sheet = get_sheet(SHEET_AKUN)

    sheet.append_row([

        str(uuid.uuid4()),

        user_id,

        data.get("gmail", ""),
        data.get("twitter", ""),
        data.get("telegram", ""),
        data.get("discord", ""),
        data.get("github", "")

    ])

    _get_all_cached.cache_clear()


# ================= DELETE =================

def delete(id, user_id):

    sheet = get_sheet(SHEET_AKUN)

    rows = sheet.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(id)
            and str(r[1]) == str(user_id)
        ):

            sheet.delete_rows(i)
            break

    _get_all_cached.cache_clear()


# ================= UPDATE =================

def update(id, data, user_id):

    sheet = get_sheet(SHEET_AKUN)

    rows = sheet.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(id)
            and str(r[1]) == str(user_id)
        ):

            sheet.update(

                f"C{i}:G{i}",

                [[
                    data.get("gmail", ""),
                    data.get("twitter", ""),
                    data.get("telegram", ""),
                    data.get("discord", ""),
                    data.get("github", "")
                ]]

            )

            break

    _get_all_cached.cache_clear()