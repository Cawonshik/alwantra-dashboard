import uuid
from flask_login import UserMixin
from database.sheets import get_sheet
from database.config import SHEET_USERS


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    # ================= GET BY ID =================
    @staticmethod
    def get(user_id):
        sheet = get_sheet(SHEET_USERS)
        rows = sheet.get_all_records()

        for r in rows:
            if r["id"] == user_id:
                return User(r["id"], r["username"])

        return None

    # ================= FIND BY USERNAME =================
    @staticmethod
    def find_by_username(username):
        sheet = get_sheet(SHEET_USERS)
        rows = sheet.get_all_records()

        for r in rows:
            if r["username"] == username:
                return r

        return None

    # ================= CREATE USER =================
    @staticmethod
    def create(username, password_hash):
        sheet = get_sheet(SHEET_USERS)

        # cek username sudah ada?
        existing = User.find_by_username(username)
        if existing:
            return False

        sheet.append_row([
            str(uuid.uuid4()),
            username,
            password_hash
        ])

        return True