import os

# ==================================================
# SPREADSHEET CONFIG
# ==================================================

# Nama Google Spreadsheet utama
SPREADSHEET_NAME = os.getenv(
    "SPREADSHEET_NAME",
    "ALWANTRA_DB"
)


# ==================================================
# SHEET NAMES
# ==================================================

# Sheet untuk user login
SHEET_USERS = "users"

# Sheet untuk data airdrop
SHEET_AIRDROP = "airdrop"

# Sheet untuk wallet address
SHEET_ADDRESS = "address"

# Sheet untuk akun social
SHEET_AKUN = "akun"