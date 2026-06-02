import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- AUTOMATED DATABASE SETUP ---
def get_db_connection():
    """Connects instantly to a localized database file without background services."""
    return sqlite3.connect("fintech_tracker.db")

def setup_database_tables():
    """Generates schema tables and basic testing boundaries automatically."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            monthly_limit REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)
    
    # Pre-seed profile tracking rows if tables are pristine
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (user_id, username, email) VALUES (1, 'Alex', 'alex@test.com')")
        cursor.execute("INSERT INTO budgets (user_id, category, monthly_limit) VALUES (1, 'Food', 1000.00)")
        cursor.execute("INSERT INTO budgets (user_id, category, monthly_limit) VALUES (1, 'Travel', 500.00)")
    connection.commit()
    connection.close()

# --- APP INTERFACE TRIGGER ACTION ---
def log_expense_action():
    """Processes entry form clicks, aggregates totals via database, and fires 90% alerts."""
    try:
        # Pull text from inputs safely
        amount_str = amount_entry.get().strip()
        if not amount_str:
            messagebox.showerror("Input Error", "Please enter an amount!")
            return
            
        amount = float(amount_str)
        category = category_var.get()
        date_str = datetime.now().strftime("%Y-%m-%d")
        user_id = 1
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert current purchase entry item row
        cursor.execute("INSERT INTO expenses (user_id, amount, category, expense_date) VALUES (?, ?, ?, ?)", 
                       (user_id, amount, category, date_str))
        connection.commit()
        
        # Calculate current aggregate sum total using SUM matrix math strings
        target_month_str = datetime.now().strftime("%Y-%m")
        cursor.execute("""
            SELECT SUM(amount) FROM expenses 
            WHERE user_id = ? AND category = ? AND strftime('%Y-%m', expense_date) = ?
        """, (user_id, category, target_month_str))
        total_spent = float(cursor.fetchone()[0] or 0.0)
        
        # Grab target tracking limit definitions
        cursor.execute("SELECT monthly_limit FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
        monthly_limit = float(cursor.fetchone()[0] or 1000.0)
        connection.close()
        
        # Refresh window status panel numbers
        status_label.config(text=f"Total Spent in '{category}': ${total_spent:.2f} / ${monthly_limit:.2f}", fg="#2c3e50")
        amount_entry.delete(0, tk.END)
        
        # If the run amount crosses the 90% alert ceiling, pop up a distinct system window!
        if total_spent >= (monthly_limit * 0.90):
            messagebox.showwarning(
                "🚨 LIVE BUDGET ALERT", 
                f"Warning! Your total expenditures in '{category}' have reached ${total_spent:.2f}.\n\nThis officially breaches 90% of your maximum allowed ${monthly_limit:.2f} budget limit!"
            )
        else:
            messagebox.showinfo("Success", f"Logged ${amount:.2f} successfully under '{category}'!")
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric value amount!")

# --- GRAPHICAL INTERFACE WORKSPACE LAYER ---
setup_database_tables()

# Initialize primary window frame
root = tk.Tk()
root.title("FinTech Expense Tracker Window")
root.geometry("450x380")
root.config(bg="#f4f6f9")

# Section: Page Title
tk.Label(root, text="Personal FinTech Dashboard", font=("Helvetica", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=20)

# Section: Category Input Element
tk.Label(root, text="Select Expense Category:", font=("Helvetica", 10), bg="#f4f6f9", fg="#7f8c8d").pack()
category_var = tk.StringVar(value="Food")
category_dropdown = tk.OptionMenu(root, category_var, "Food", "Travel")
category_dropdown.config(width=12, font=("Helvetica", 10))
category_dropdown.pack(pady=5)

# Section: Price Entry Box
tk.Label(root, text="Enter Transaction Amount ($):", font=("Helvetica", 10), bg="#f4f6f9", fg="#7f8c8d").pack()
amount_entry = tk.Entry(root, font=("Helvetica", 12), width=15, justify="center")
amount_entry.pack(pady=5)

# Section: Form Execution Action Button (FIXED: Changed px/py parameters to padx/pady)
submit_btn = tk.Button(root, text="Log Expense & Run Audit", font=("Helvetica", 11, "bold"), bg="#3498db", fg="white", bd=0, padx=15, pady=7, command=log_expense_action)
submit_btn.pack(pady=20)

# Section: Runtime Status Display Dashboard Log Pane
status_label = tk.Label(root, text="Total Spent in 'Food': $0.00 / $1000.00", font=("Helvetica", 11, "italic"), bg="#f4f6f9", fg="#95a5a6")
status_label.pack(pady=15)

# Render background lifecycle window
root.mainloop()