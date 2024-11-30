# Expense Tracker CLI

A simple command-line interface application to track your daily expenses, manage budgets, and view expense summaries.

This is one of the exercises at roadmap.sh   
[Link to the project](https://roadmap.sh/projects/expense-tracker)

## Features

- Add new expenses with categories and descriptions
- List all recorded expenses
- Delete expenses by ID
- View expense summaries filtered by month or category
- Set and manage monthly budgets
- Automatic budget tracking and overspending alerts
- Persistent storage using CSV for expenses and JSON for budget

## Prerequisites

- Python 3.x
- Required Python packages:
  - tabulate
  - argparse (included in Python standard library)
  - json (included in Python standard library)
  - csv (included in Python standard library)
  - datetime (included in Python standard library)
  - pathlib (included in Python standard library)

## Installation

1. Clone this repository or download the source code
2. Install the required package:
   ```bash
   pip install tabulate
   ```

## Usage

### Adding an Expense
```bash
python expense_tracker.py add --category "Food" "Lunch at restaurant" 25.50
```

### Listing All Expenses
```bash
python expense_tracker.py list
```

### Deleting an Expense
```bash
python expense_tracker.py delete 1
```

### Viewing Expense Summary
View all expenses for a specific month:
```bash
python expense_tracker.py summary --month 3  # March
```

View expenses by category:
```bash
python expense_tracker.py summary --category "Food"
```

### Setting Monthly Budget
Set a monthly budget:
```bash
python expense_tracker.py budget 1000
```

Remove budget tracking:
```bash
python expense_tracker.py budget 0
```

## Data Storage

- Expenses are stored in `records.csv`
- Budget information is stored in `budget.json`
- Both files are created automatically when you first use the application

## Command Reference

| Command | Description | Required Arguments | Optional Arguments |
|---------|-------------|-------------------|-------------------|
| `add` | Add a new expense | `description`, `amount` | `--category` |
| `list` | Display all expenses | None | None |
| `delete` | Remove an expense | `id` | None |
| `summary` | View expense summary | None | `--month`, `--category` |
| `budget` | Set monthly budget | `budget_amount` | None |

## Features Details

### Expense Categories
- Categories are automatically capitalized
- Categories are optional when adding expenses

### Budget Tracking
- The system will alert you when you exceed your monthly budget
- Budget can be disabled by setting it to 0
- Budget tracking is done on a monthly basis

### Date Handling
- Dates are automatically recorded when adding expenses
- Date format: DD/Mon/YYYY

## File Structure
```
expense-tracker/
├── expense_tracker.py
├── records.csv        # Created automatically
└── budget.json       # Created automatically
```