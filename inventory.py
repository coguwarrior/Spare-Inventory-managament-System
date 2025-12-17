import pandas as pd
from datetime import datetime
from pathlib import Path

# ================= CONFIG =================
EXCEL_FILE = "SPARES_MASTER.xlsx"
MASTER_SHEET = "MASTER"
LOG_SHEET = "TRANSACTION_LOG"


# ================= CORE LOADERS =================
def load_master():
    if not Path(EXCEL_FILE).exists():
        raise Exception("Excel file not found")
    return pd.read_excel(EXCEL_FILE, sheet_name=MASTER_SHEET)


def save_master(df):
    try:
        with pd.ExcelWriter(
            EXCEL_FILE,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:
            df.to_excel(writer, sheet_name=MASTER_SHEET, index=False)
    except PermissionError:
        raise Exception(
            "Excel file is OPEN.\nPlease close SPARES_MASTER.xlsx and retry."
        )


def load_log():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=LOG_SHEET)
    except:
        return pd.DataFrame(columns=[
            "Date", "User", "Action", "Item_ID",
            "Part_Name", "Qty_Before", "Qty_Change", "Qty_After"
        ])


def save_log(df):
    try:
        with pd.ExcelWriter(
            EXCEL_FILE,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:
            df.to_excel(writer, sheet_name=LOG_SHEET, index=False)
    except PermissionError:
        raise Exception(
            "Excel file is OPEN.\nPlease close SPARES_MASTER.xlsx and retry."
        )


# ================= RESOLUTION =================
def get_item_by_part_no(part_no):
    df = load_master()
    row = df[df["Part_No"].str.upper() == part_no.upper()]
    if row.empty:
        raise Exception("Part Number not found")
    return row.iloc[0]


# ================= ISSUE / RECEIVE =================
def issue_by_part_no(part_no, qty, user):
    if qty <= 0:
        raise Exception("Invalid quantity")

    df = load_master()
    item = get_item_by_part_no(part_no)
    idx = df[df["Item_ID"] == item["Item_ID"]].index[0]

    available = int(df.at[idx, "Qty_Available"])
    if qty > available:
        raise Exception("Insufficient stock")

    df.at[idx, "Qty_Available"] = available - qty
    df.at[idx, "Last_Updated"] = datetime.now()
    save_master(df)

    log = load_log()
    log.loc[len(log)] = [
        datetime.now(), user, "ISSUE",
        item["Item_ID"], item["Part_Name"],
        available, -qty, available - qty
    ]
    save_log(log)


def receive_by_part_no(part_no, qty, user):
    if qty <= 0:
        raise Exception("Invalid quantity")

    df = load_master()
    item = get_item_by_part_no(part_no)
    idx = df[df["Item_ID"] == item["Item_ID"]].index[0]

    before = int(df.at[idx, "Qty_Available"])
    df.at[idx, "Qty_Available"] = before + qty
    df.at[idx, "Last_Updated"] = datetime.now()
    save_master(df)

    log = load_log()
    log.loc[len(log)] = [
        datetime.now(), user, "RECEIPT",
        item["Item_ID"], item["Part_Name"],
        before, qty, before + qty
    ]
    save_log(log)


# ================= SEARCH =================
def search_spares(keyword):
    df = load_master()
    k = keyword.lower()
    return df[
        df["Part_Name"].str.lower().str.contains(k, na=False) |
        df["Part_No"].str.lower().str.contains(k, na=False) |
        df["Equipment"].str.lower().str.contains(k, na=False) |
        df["Location"].str.lower().str.contains(k, na=False)
    ]


def search_by_part_no(part_no):
    df = load_master()
    return df[df["Part_No"].str.contains(part_no, case=False, na=False)]


def search_by_equipment(equipment):
    df = load_master()
    return df[df["Equipment"].str.contains(equipment, case=False, na=False)]


# ================= LOW STOCK =================
def get_low_stock_items():
    df = load_master()
    return df[df["Qty_Available"] <= df["Min_Qty"]]


def low_stock_alert():
    low = get_low_stock_items()
    return None if low.empty else low


# ================= SUMMARY =================
def stock_summary():
    return load_master()


# ================= TRANSACTION HISTORY =================
def get_transaction_history():
    return load_log()


# ================= FORECAST =================
def annual_demand_forecast(item_id, months=12):
    log = load_log()
    if log.empty:
        return 0

    log["Date"] = pd.to_datetime(log["Date"])
    cutoff = datetime.now() - pd.DateOffset(months=months)

    issues = log[
        (log["Item_ID"] == item_id) &
        (log["Action"] == "ISSUE") &
        (log["Date"] >= cutoff)
    ]

    if issues.empty:
        return 0

    total_issued = -issues["Qty_Change"].sum()
    return int((total_issued / months) * 12)
