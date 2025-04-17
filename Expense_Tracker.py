import sqlite3
import tkinter as tk
from tkinter import ttk

# Setup SQLite DB
def setup_sql_db():
    connection =sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(sl_num INTEGER PRIMARY KEY,
                expense_name TEXT NOT NULL, amount INTEGER,Date TEXT)''')
    connection.commit()
    connection.close()

def add_expense():
    # Get user input from entry fields
    name = expense_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if name and amount and date:
        try:
            connection =sqlite3.connect("expenses.db")
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO expenses (expense_name, amount, Date)
                                        VALUES (?, ?, ?)''', (name, int(amount), date))
            connection.commit()
            connection.close()

            result_label.config(text="✅Expense added Successfully!",fg ="green")
            expense_entry.delete(0,tk.END)
            amount_entry.delete(0,tk.END)
            date_entry.delete(0,tk.END)
            show_expenses()
        except Exception as e :
            result_label.config(text=f"Error: {e}", fg="red")
    else :
         result_label.config(text="⚠️ Please fill all fields!", fg="red")

def show_expenses():
    for row in tree.get_children():
        tree.delete(row)

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    connection.close()

    
    for row in rows:
        tree.insert("",tk.END, values=row)

def delete_selected_expense():
    selected_item = tree.selection()
    if not selected_item :
        result_label.config(text="⚠️Please select a row to delete",fg="red")
        return
    
    expense_id = tree.item(selected_item)["values"][0]
    try:
        connection =sqlite3.connect("expenses.db")
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM expenses WHERE Sl_num=?''',(expense_id,))
        connection.commit()
        connection.close()

        tree.delete(selected_item)
        result_label.config(text="🚮Deleted Successfully!",fg ="green")
    except Exception as e :
        result_label.config(text="Error",fg="red")
setup_sql_db()
# Create  a main window
root = tk.Tk()
root.title("Welcome to Your Expense Tracker 📉")
root.geometry("500x450")

## Title Label
title_label= tk.Label(root, text="Enter the Details", font=("Arial",15,"bold"))
title_label.pack(pady =10)

# Create labels
tk.Label(root,text="Expense_name",font=("Arial",12,"bold"),fg="white",bg="blue").pack()
expense_entry = tk.Entry(root)
expense_entry.pack(pady=5)

tk.Label(root,text="Amount",font=("Arial",12,"bold"),fg="white",bg="blue").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

tk.Label(root,text="Date",font=("Arial",12,"bold"),fg="white",bg="blue").pack()
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

result_label=tk.Label(root, text="", font=("Arial",15,"bold"))
result_label.pack(pady =10)

#craete a button
tk.Button(root, text="Add Expenses",command = add_expense,font=("Calibri",15,"bold"),fg="yellow",bg="green", bd=4).pack(pady =10)
tk.Button(root, text="Show All Expenses", command=show_expenses, font=("Calibri", 15, "bold"), fg="yellow", bg="purple", bd=4).pack(pady=10)
tk.Button(root, text="Delete Selected Expense", command=delete_selected_expense, font=("Calibri", 15, "bold"), fg="yellow", bg="purple", bd=4).pack(pady=10)

# Create Treeview for displaying expenses
columns = ("ID", "Name", "Amount", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

# Setup columns and headings for the treeview
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(pady=10, fill=tk.X)

# Initial call to show expenses on startup (if any)
show_expenses()

#create a main loop
show_expenses()
root.mainloop()
