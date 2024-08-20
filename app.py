import tkinter as tk
import csv
from user_interface import ExpenseTrackerUI

class ExpenseTracker:
    def __init__(self, root):
        self.ui = ExpenseTrackerUI(root, self.add_expense, self.view_expenses, self.calculate_totals, self.delete_expense, self.update_expense)
    
    def view_expenses(self):
        try:
            with open('expenses.csv', 'r') as file:
                expenses = list(csv.reader(file))
                self.ui.populate_expense_display(["{0}, {1}, {2}, ${3}".format(*expense) for expense in expenses])
        except FileNotFoundError:
            self.ui.show_error("No expenses found!")

    def delete_expense(self):
        try:
            index = self.ui.expense_list.curselection()[0]
            with open('expenses.csv', 'r') as file:
                expenses = list(csv.reader(file))
            expenses.pop(index)
            with open('expenses.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(expenses)
            self.view_expenses()
        except IndexError:
            self.ui.show_error("No expense selected")


    def add_expense(self):
        date, category, description, amount = self.ui.get_inputs()
        data = [date, category, description, amount]
        with open('expenses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        self.ui.show_message("Expense added successfully!")
        self.ui.clear_inputs()

    def calculate_totals(self):
        try:
            with open('expenses.csv', 'r') as file:
                total = sum(float(row[3]) for row in csv.reader(file))
                self.ui.show_message(f"Total expenses: ${total:.2f}")
        except FileNotFoundError:
            self.ui.show_error("No expenses to calculate!")
    
    def update_expense(self, index, updated_expense):
        updated_expense = self.ui.get_inputs()
        with open('expenses.csv', 'r') as file:
            expenses = list(csv.reader(file))
        expenses[index] = updated_expense
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(expenses)
        self.ui.populate_expense_display(["{0}, {1}, {2}, ${3}".format(*expense) for expense in expenses])

    def edit_expense(self, index):
        # This assumes you need to perform some logic in the backend before editing
        # Fetch expense details, possibly do some validation or additional logic
        expense_details = self.fetch_expense_details(index)
        self.ui.load_expense_into_fields(expense_details)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
