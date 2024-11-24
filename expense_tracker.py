import sys
import argparse
import csv
from datetime import datetime
from pathlib import Path

"""Initialize expense records and budget"""
records = []
monthly_budget = None
file_path = "records.csv"

"""Load existing expense records from file if it exists"""
if Path(file_path).exists():
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append({
                "ID": int(row[0]), 
                "Date": row[1], 
                "Category": row[2], 
                "Description": row[3], 
                "Amount": float(row[4])
            })


def main():
    """Check valid command-line argument"""
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")
    
    command = sys.argv[1]
    VALID_COMMAND = ["add", "list", "summary", "delete", "set-budget", "export"]

    if command not in VALID_COMMAND:
        sys.exit(f"Program only accepts the following command {VALID_COMMAND}")

    """Parse command-line with functions"""
    try:
        if command == "add":
            if len(sys.argv) < 5 or len(sys.argv) > 5:
                sys.exit("Usage: expense_tracker.py add <expense_category> <expense_description> <expense_amount>")
            else:
                expense_add(sys.argv[2], sys.argv[3], sys.argv[4])
    except Exception:
        sys.exit("Missing or invalid command-line arguments")


def expense_save():
    """Save records to the CSV file"""
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Date", "Category", "Description", "Amount"])
        writer.writeheader()
        writer.writerows(records)


def expense_add(category, description, amount):
    """Validate amount"""
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
    except ValueError as e:
        sys.exit(f"Invalid amount: {e}")

    """Create new record"""
    expense_id = len(records) + 1
    now = datetime.now()
    records.append({
        "ID": expense_id,
        "Date": now.strftime("%d/%b/%Y"),
        "Category": category,
        "Description": description,
        "Amount": amount
    })
    expense_save()
    print(f"Expense added successfully (ID: {expense_id})")

    """Check if expenses exceed the monthly budget"""
    if monthly_budget is not None:
        current_month = now.month()
        current_year = now.year()
        this_month_expense = 0
        for record in records:
            if datetime.strptime(record["Date"], "%d/%b/%Y").month() == current_month and datetime.strptime(record["Date"], "%d/%b/%Y").month() == current_year:
                this_month_expense += record["Amount"]
        if this_month_expense > monthly_budget:
            print(f"Expense already exceeded this month budget. Current total: {this_month_expense}")


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


if __name__ == "__main__":
    main()