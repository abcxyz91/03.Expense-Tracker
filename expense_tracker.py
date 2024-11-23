import sys
import argparse
import csv
from datetime import datetime
from pathlib import Path

"""Open expense record file"""
records = []
with open("records.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        records.append({"ID": row[0], "Date": row[1], "Category": row[2], "Description": row[3], "Amount": row[4]})

"""Setup monthly budget"""
monthly_budget = None

def main():
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")
    
    command = sys.argv[1]

    VALID_COMMAND = ["add", "list", "summary", "delete", "set-budget", "export"]
    if command not in VALID_COMMAND:
        sys.exit(f"Program only accepts the following command {VALID_COMMAND}")

    try:
        if command == "add":
            if len(sys.argv) < 5 or len(sys.argv) > 5:
                sys.exit("Usage: expense_tracker add <expense_category> <expense_description> <expense_amount>")
            else:
                expense_add(sys.argv[2], sys.argv[3], sys.argv[4])
    except Exception:
        sys.exit("Missing or invalid command-line arguments")


def expense_save():
    pass


def expense_add(category, description, amount):
    expense_id = len(records) + 1
    now = datetime.now()
    records.append({
        "ID": expense_id,
        "Date": now.strftime("%d/%b/%Y")
        "Category": category,
        "Description": description,
        "Amount": float(amount)
    })
    expense_save()
    print(f"Expense added successfully (ID: {expense_id})")

    """Check if the total expense amount of this month exceed the budget or not"""
    total_month_expense = 0
    for record in records:
        if record["Date"] == now.month():
            total_month_expense += record["Amount"]
    if total_month_expense > monthly_budget and monthly_budget not None:
        print(f"Expense already exceeded this month budget")


def expense_list():
    pass


def expense_summary():
    pass


def expense_delete():
    pass


def expense_set_budget():
    pass


def expense_export():
    pass