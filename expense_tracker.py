import json
import argparse
import csv
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

"""Initialize expense records and budget"""
records = []
records_path = "records.csv"
budget_path = "budget.json"

"""Setup a dictonary for months"""
months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

"""Load existing expense records from file if it exists"""
if Path(records_path).exists():
    with open(records_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append({
                "ID": int(row["ID"]), 
                "Date": row["Date"], 
                "Category": row["Category"], 
                "Description": row["Description"], 
                "Amount": float(row["Amount"])
            })

"""Load existing budget info from json file if it exists"""
if Path(budget_path).exists():
    with open(budget_path, "r") as file:
        budget = json.load(file)
        if budget:
            monthly_budget = float(budget["monthly_budget"])
else:
    budget = {}
    monthly_budget = None

def main():
    """Setup main parser with description"""
    parser = argparse.ArgumentParser(description="Simple CLI to track your expense")

    """Setup subparsers for different commands"""
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    """Parser for add command and its required and optional arguments"""
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--category", type=str, help="Expense category")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=float, help="Expense amount")

    """Parser for list command with no additional argument"""
    subparsers.add_parser("list", help="List all the expenses")

    """Parser for delete command and its required argument"""
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int, help="Expense ID to delete")

    """Parser for summary and its optional argument"""
    summary_parser = subparsers.add_parser("summary", help="Summary expenses")
    summary_parser.add_argument("--month", type=int, help="Summary by month (1-12)")
    summary_parser.add_argument("--category", type=str, help="Summary by category")

    """Parser for set budget command and its argument"""
    budget_parser = subparsers.add_parser("budget", help="Set a monthly budget. 0 means no budget")
    budget_parser.add_argument("budget_amount", type=float, help="Budget amount")

    """Parse all arguments"""
    args = parser.parse_args()

    """Call the functions based on user command"""
    if args.command == "add":
        expense_add(args.category, args.description, args.amount)
    elif args.command == "list":
        expense_list()
    elif args.command == "delete":
        expense_delete(args.id)
    elif args.command == "summary":
        expense_summary(args.month, args.category)
    elif args.command == "budget":
        expense_set_budget(args.budget_amount)


def expense_save():
    """Save records to the CSV file"""
    try:
        with open(records_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Date", "Category", "Description", "Amount"])
            writer.writeheader()
            writer.writerows(records)
    except IOError as e:
        print(f"Error saving record: {e}")


def expense_add(category, description, amount):
    """Validate amount"""
    if not description.strip():
        raise ValueError("Expense must have a description")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

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
        current_month = now.month
        current_year = now.year
        this_month_expense = 0
        for record in records:
            if datetime.strptime(record["Date"], "%d/%b/%Y").month == current_month and datetime.strptime(record["Date"], "%d/%b/%Y").year == current_year:
                this_month_expense += float(record["Amount"])
        if this_month_expense > monthly_budget:
            print(f"Expense already exceeded this month budget. Current total: {this_month_expense}")


def expense_list():
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No expense recorded")


def expense_summary(month=None, category=None):
    """Setup variables"""
    now = datetime.now()
    current_year = now.year
    total_expense = 0
    filtered_records = []

    """Check the arguments and append record into filtered_records"""
    if month is not None:
        if month < 1 or month > 12:
            raise ValueError("Month must be within 1-12")
        
    for record in records:
        record_date = datetime.strptime(record["Date"], "%d/%b/%Y")
        if record_date.year != current_year:
            continue
        if month is not None and record_date.month != month:
            continue
        if category is not None and record["Category"] != category.title():
            continue
        filtered_records.append(record)
        
    """Calculate the total_expense and print the result"""
    if filtered_records:
        for record in filtered_records:
            total_expense += record["Amount"]
        print(tabulate(filtered_records, headers="keys", tablefmt="grid"))
        print(f"Total expenses that match current criteria: ${total_expense}")
    else:
        print("There are no expenses match the current criteria")


def expense_delete(id):
    """Delete existing record id"""
    for i, record in enumerate(records):
        if record["ID"] == id:
            del records[i]
            expense_save()
            print(f"Expense {id} deleted sucessfully")
            return
    else:
        print("Expense not found")


def expense_set_budget(amount):
    """Set this function to use the global monthly_budget variable"""
    global monthly_budget

    """Setup monthly budget"""
    if amount < 0:
        raise ValueError("Budget amount must be a positive number")
    with open(budget_path, "w") as file:
        if amount != 0:
            budget = {"monthly_budget": amount}
            monthly_budget = amount
            print(f"Budget is set to ${amount}")
        else:
            """Remove key if amount is set to 0"""
            budget = {}
            monthly_budget = None
            print("Budget removed")
        json.dump(budget, file, indent=2)


if __name__ == "__main__":
    main()