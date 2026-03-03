from database.sheets import init_sheet
from database.config import *

def init_db():
    print("🚀 Initializing Database...")

    # ================= USERS =================
    init_sheet(SHEET_USERS, [
        "id",
        "username",
        "password"
    ])

    # ================= AIRDROP =================
    init_sheet(SHEET_AIRDROP, [
        "id",
        "user_id",
        "name",
        "type",
        "chain",
        "wallet",
        "channel",
        "note",
        "status",
        "date"
    ])

    # ================= ADDRESS =================
    init_sheet(SHEET_ADDRESS, [
        "id",
        "user_id",
        "nomor",
        "evm",
        "sol",
        "sui"
    ])

    # ================= AKUN =================
    init_sheet(SHEET_AKUN, [
        "id",
        "user_id",
        "gmail",
        "twitter",
        "telegram",
        "discord",
        "github"
    ])

    print("✅ Database Ready")