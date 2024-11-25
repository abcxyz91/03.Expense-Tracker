import sys
import argparse
import csv
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

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
                "ID": int(row["ID"]), 
                "Date": row["Date"], 
                "Category": row["Category"], 
                "Description": row["Description"], 
                "Amount": float(row["Amount"])
            })


def main():
    """Setup main parser with description"""
    parser = argparse.ArgumentParser(description="Simple CLI to track your expense")

    """Setup subparsers for different commands"""
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    """Parser for add command and its required and optional arguments"""
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("category", type=str, help="Expense category")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=float, help="Expense amount")

    """Parser for list command with no additional argument"""
    subparsers.add_parser("list", help="List all the expenses")

    """Parser for delete command and its required argument"""
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int, help="Expense ID to delete")

    """Parse all arguments"""
    args = parser.parse_args()

    """Call the functions based on user command"""
    if args.command == "add":
        expense_add(args.category, args.description, args.amount)
    elif args.command == "list":
        expense_list()
    elif args.command == "delete":
        expense_delete(args.id)


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
        "Category": category.title(),
        "Description": description.title(),
        "Amount": f"{amount:.2f}"
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
    print(tabulate(records, headers="keys", tablefmt="grid"))


def expense_summary():
    pass


def expense_delete(id):
    """Delete existing record id"""
    try:
        record_id = int(id)
    except ValueError:
        sys.exit("Invalid id number")
    else:
        for i, record in enumerate(records):
            if record["ID"] == record_id:
                del records[i]
                expense_save()
                print(f"Expense {id} deleted sucessfully")
                break
        else:
            print("Expense not found")


def expense_set_budget():
    pass


def expense_export():
    pass


if __name__ == "__main__":
    main()