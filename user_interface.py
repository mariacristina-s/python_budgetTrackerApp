import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ExpenseTrackerUI:
    def __init__(self, master, add_expense_callback, view_expenses_callback, calculate_totals_callback, delete_expense_callback, update_expense_callback):
        self.master = master
        master.title("Expense Tracker")

        # Setup fields
        ttk.Label(master, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date = ttk.Entry(master)
        self.date.grid(row=0, column=1)

        ttk.Label(master, text="Category:").grid(row=1, column=0)
        self.category = ttk.Entry(master)
        self.category.grid(row=1, column=1)

        ttk.Label(master, text="Description:").grid(row=2, column=0)
        self.description = ttk.Entry(master)
        self.description.grid(row=2, column=1)

        ttk.Label(master, text="Amount ($):").grid(row=3, column=0)
        self.amount = ttk.Entry(master)
        self.amount.grid(row=3, column=1)

        self.add_expense_callback = add_expense_callback
        self.view_expenses_callback = view_expenses_callback
        self.calculate_totals_callback = calculate_totals_callback
        self.delete_expense_callback = delete_expense_callback
        self.update_expense_callback = update_expense_callback

        # Buttons
        ttk.Button(master, text="Add Expense", command=add_expense_callback).grid(row=4, column=0)
        ttk.Button(master, text="View Expenses", command=view_expenses_callback).grid(row=4, column=1)
        ttk.Button(master, text="Calculate Totals", command=calculate_totals_callback).grid(row=5, column=0)
        ttk.Button(master, text="Exit", command=master.quit).grid(row=5, column=1)
        ttk.Button(master, text="Edit Selected Expense", command=lambda: self.edit_expense(self.expense_list.curselection()[0])).grid(row=7, column=0)
        ttk.Button(master, text="Delete Selected Expense", command=delete_expense_callback).grid(row=7, column=1)

        # Text widget for displaying expenses
        self.expense_list = tk.Listbox(master, height=10, width=50)
        self.expense_list.grid(row=6, column=0, columnspan=2, pady=10)
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.expense_list.yview)
        self.scrollbar.grid(row=6, column=2, sticky='ns')
        self.expense_list.config(yscrollcommand=self.scrollbar.set)


    def get_inputs(self):
        return self.date.get(), self.category.get(), self.description.get(), self.amount.get()

    def clear_inputs(self):
        self.date.delete(0, tk.END)
        self.category.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.amount.delete(0, tk.END)

    def show_expenses(self, expenses):
        self.expense_display.delete('1.0', tk.END)  # Clear previous contents
        self.expense_display.insert(tk.END, expenses)

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def populate_expense_display(self, expenses):
        self.expense_list.delete(0, tk.END)
        for expense in expenses:
            self.expense_list.insert(tk.END, expense)

    def edit_expense(self, index):
        try:
            selected_expense = self.expense_list.get(index)
            date, category, description, amount = selected_expense.split(', ')
            self.date.delete(0, tk.END)
            self.date.insert(0, date.strip())
            self.category.delete(0, tk.END)
            self.category.insert(0, category.strip())
            self.description.delete(0, tk.END)
            self.description.insert(0, description.strip())
            self.amount.delete(0, tk.END)
            self.amount.insert(0, amount.strip().replace('$', ''))

            # Setup the Update Expense button
            if hasattr(self, 'update_button'):
                self.update_button.destroy()  # Ensure only one update button exists
            self.update_button = ttk.Button(self.master, text="Update Expense", command=lambda: self.update_expense_callback(self.expense_list.curselection()[0], self.get_inputs()) if self.expense_list.curselection() else messagebox.showwarning("Update Error", "No expense selected"))
            self.update_button.grid(row=8, column=0, columnspan=2)
        except IndexError:
            messagebox.showerror("Selection Error", "No expense selected")

    