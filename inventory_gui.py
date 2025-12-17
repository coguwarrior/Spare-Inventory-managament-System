import tkinter as tk
from tkinter import ttk, messagebox

from inventory import (
    issue_by_part_no,
    receive_by_part_no,
    search_spares,
    search_by_part_no,
    search_by_equipment,
    get_low_stock_items,
    stock_summary,
    annual_demand_forecast,
    get_transaction_history,
    low_stock_alert
)

from auth import authenticate

current_user = None
current_role = None


# =================================================
# MAIN UI
# =================================================
def launch_main_ui():
    root = tk.Tk()
    root.title(f"Offline Spare Inventory System | User: {current_user}")
    root.geometry("500x650")

    # ---------- TABLE VIEW ----------
    def show_table(title, df):
        if df is None or df.empty:
            messagebox.showinfo("Info", "No records found")
            return

        win = tk.Toplevel(root)
        win.title(title)
        win.geometry("1050x420")

        tree = ttk.Treeview(win, columns=list(df.columns), show="headings")

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack(fill=tk.BOTH, expand=True)

    # ---------- ACTIONS ----------
    def issue_action():
        try:
            issue_by_part_no(part_no.get().strip(), int(qty.get()), current_user)
            messagebox.showinfo("Success", "Spare issued successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def receive_action():
        try:
            receive_by_part_no(part_no.get().strip(), int(qty.get()), current_user)
            messagebox.showinfo("Success", "Spare received successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_general():
        show_table("Search Results", search_spares(search_entry.get()))

    def search_part():
        show_table("Search by Part Number", search_by_part_no(search_entry.get()))

    def search_equipment_ui():
        show_table("Search by Equipment", search_by_equipment(search_entry.get()))

    def show_low_stock():
        show_table("Low Stock Spares", get_low_stock_items())

    def show_summary():
        show_table("Stock Summary", stock_summary())

    def show_forecast():
        try:
            demand = annual_demand_forecast_by_part(part_no.get().strip())
            messagebox.showinfo("Forecast", f"Annual Demand: {demand}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_transactions():
        show_table("Transaction History", get_transaction_history())

    def startup_alert():
        if low_stock_alert() is not None:
            show_low_stock()

    # ---------- UI ----------
    tk.Label(root, text=f"Logged in as: {current_user} ({current_role})",
             font=("Arial", 10, "bold")).pack(pady=5)

    # Search
    tk.Label(root, text="Search").pack()
    search_entry = tk.Entry(root, width=30)
    search_entry.pack()

    tk.Button(root, text="Search (General)", command=search_general).pack(pady=2)
    tk.Button(root, text="Search by Part No", command=search_part).pack(pady=2)
    tk.Button(root, text="Search by Equipment", command=search_equipment_ui).pack(pady=2)
    tk.Button(root, text="🔔 Low Stock Spares", command=show_low_stock).pack(pady=6)

    # Issue / Receive
    tk.Label(root, text="Part Number").pack()
    part_no = tk.Entry(root)
    part_no.pack()

    tk.Label(root, text="Quantity").pack()
    qty = tk.Entry(root)
    qty.pack()

    tk.Button(root, text="Issue Spare", command=issue_action).pack(pady=3)
    tk.Button(root, text="Receive Spare", command=receive_action).pack(pady=3)

    # Management
    tk.Button(root, text="📜 Transaction History", command=show_transactions).pack(pady=8)
    tk.Button(root, text="📦 Stock Summary", command=show_summary).pack(pady=3)

    root.after(800, startup_alert)
    root.mainloop()


# =================================================
# LOGIN
# =================================================
def login():
    global current_user, current_role

    role = authenticate(username_entry.get(), password_entry.get())
    if not role:
        messagebox.showerror("Login Failed", "Invalid credentials")
        return

    current_user = username_entry.get()
    current_role = role

    login_window.destroy()
    launch_main_ui()


login_window = tk.Tk()
login_window.title("Login - Spare Inventory System")
login_window.geometry("300x220")

tk.Label(login_window, text="Username").pack(pady=6)
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack(pady=6)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=login, width=15).pack(pady=18)
login_window.mainloop()
