Offline Spare Inventory Management System (SIMS)

An offline, Excel-backed Spare Inventory Management System built using Python and Tkinter, designed for ships, units, workshops, and establishments where internet access is restricted or unavailable.

The system provides secure login, controlled issue/receipt, low-stock alerts, and complete transaction history, all while keeping Excel as the backend for transparency and auditability.

✨ Key Features
🔐 Authentication

Login-based access

Two predefined roles:

MCERA – Officer / Admin

MCEAP – Storekeeper

📦 Inventory Operations

Issue spares by Part Number

Receive spares by Part Number

Real-time stock update

Prevents over-issuing

🔍 Search & Visibility

Search by:

Part Name

Part Number

Equipment Name

View all spares

View low-quantity / critical spares

🔔 Alerts

Automatic low-stock alert popup on startup

Threshold controlled per item (Min_Qty)

📜 Transaction History

Complete issue/receipt log

Timestamped, user-tagged

Read-only audit trail

📊 Management Utilities

Stock summary (current state)

Annual demand forecast (based on past issues)

📴 Fully Offline

No internet required

Excel used as backend

Suitable for isolated or secure systems

🧱 System Architecture
Tkinter UI
    |
    v
inventory_gui.py  →  inventory.py  →  SPARES_MASTER.xlsx
                         |
                         └── TRANSACTION_LOG (Audit Trail)

📁 Project Structure
SIMS/
│
├── inventory_gui.py        # Tkinter GUI
├── inventory.py            # Backend logic
├── auth.py                 # Login & authentication
├── requirements.txt        # Python dependencies
├── SPARES_MASTER.xlsx      # Excel backend
└── README.md

🧩 Excel Backend Structure
📘 Sheet 1: MASTER (Mandatory)

Column headers (must match exactly):

Item_ID
Equipment
Part_Name
Part_No
Qty_Available
Min_Qty
Unit
Location
Last_Updated

📕 Sheet 2: TRANSACTION_LOG (Auto-managed)
Date
User
Action
Item_ID
Part_Name
Qty_Before
Qty_Change
Qty_After

⚙️ Installation (Developer Mode)
1️⃣ Clone the repository
git clone https://github.com/coguwarrior/Spare-Inventory-managament-System.git
cd Spare-Inventory-managament-System

2️⃣ Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate   # Git Bash

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python inventory_gui.py

▶️ Installation (End User – EXE)

Download:

inventory_gui.exe

SPARES_MASTER.xlsx

Keep both in the same folder

Double-click the .exe

No Python installation required

🔑 Login Credentials (Default)
Username	Password	Role
MCERA	mcera@123	Officer / Admin
MCEAP	mceap@123	Storekeeper

⚠️ Recommended: Change passwords before deployment.

🧭 Usage Instructions
🔍 Search Spares

Enter keyword

Search by:

General

Part Number

Equipment

View results in table

📦 Issue Spare

Enter Part Number

Enter quantity

Click Issue Spare

Stock updates instantly

📥 Receive Spare

Enter Part Number

Enter quantity

Click Receive Spare

🔔 Low Stock Monitoring

Automatic alert on startup

Manual view via Low Stock Spares

📜 Transaction History

Click Transaction History

View all issue/receipt records

🖼️ Screenshots

📌 Add screenshots here after deployment

Suggested screenshots:

Login screen

Main dashboard

Search results

Issue/Receipt screen

Low stock alert popup

Transaction history window

![Login Screen](screenshots/login.png)
![Main UI](screenshots/main_ui.png)
![Low Stock Alert](screenshots/low_stock.png)

🛡️ Operational Notes

Do not keep Excel open while issuing/receiving spares

Use Excel only for:

Backup

Reports

Inspection reference

All operations should be done via the application

🚀 Future Enhancements

Role-based permissions (read-only / issue-only)

Password hashing

Dropdown-based item selection

Monthly consumption reports

Barcode / QR-based issuing

Auto-reorder suggestions

📄 License

This project is intended for educational, internal, and operational use.
Customization and redistribution permitted as per organisational policy.

👤 Author

Developed by:
Palani Rajeshwar
GitHub: https://github.com/coguwarrior

✅ STATUS

✔ Feature complete
✔ Offline ready
✔ Audit compliant
✔ Deployment ready

If you want, next I can:
