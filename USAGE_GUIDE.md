SuperPy Usage Guide with Examples
=================================

SuperPy is a command-line inventory manager for small businesses. Use it to track purchases, sales, and performance.

--------------------------------------------------------------------------------
1. Set or Advance the Current Date
--------------------------------------------------------------------------------

SuperPy keeps an internal "current date" for timestamping all actions.

Set the current date:
    Command:
        python superpy.py --set-date 2025-06-01
    Output:
        OK

Advance the date by a number of days:
    Command:
        python superpy.py --advance-time 5
    Output:
        OK

--------------------------------------------------------------------------------
2. Buy Products
--------------------------------------------------------------------------------

Records a product purchase and updates inventory.

Command:
    python superpy.py buy --product-name milk --price 1.25 --count 10 --expiration-date 2025-06-10

Meaning:
    You bought 10 units of milk at $1.25 each, expiring on June 10, 2025.

Command (with default count = 1):
    python superpy.py buy --product-name bread --price 2.50 --expiration-date 2025-06-07

Output:
    Ordered 1 unit of bread.


--------------------------------------------------------------------------------
3. Sell Products
--------------------------------------------------------------------------------

Sells a product from inventory using FIFO logic.

Command:
    python superpy.py sell --product-name milk --count 3

Meaning:
    Sells 3 units of milk from the oldest available stock.

Output:
    Successfully sold 3 units of milk.

If stock is insufficient:
    Output:
        Not enough stock to sell 5 milk(s).

--------------------------------------------------------------------------------
4. Report Commands
--------------------------------------------------------------------------------

Generate reports for inventory, revenue, or profit.

=== Inventory Reports ===

Current inventory:
    python superpy.py report inventory --now

Inventory as of yesterday:
    python superpy.py report inventory --yesterday

Inventory on a specific date:
    python superpy.py report inventory --date 2025-06-01

Example output:
    ['id', 'product_name', 'price', 'count', 'expiration_date']
    ['1', 'milk', '1.25', '7', '2025-06-10']
    ['2', 'bread', '2.50', '1', '2025-06-07']

=== Revenue Reports ===

Today's revenue:
    python superpy.py report revenue --now

Revenue from a past date:
    python superpy.py report revenue --date 2025-06-01

Example output:
    Today's revenue so far: 3.75

=== Profit Reports ===

Profit for yesterday:
    python superpy.py report profit --yesterday

Example output:
    Yesterday's profit: 1.25

--------------------------------------------------------------------------------
5. Helpful Tips
--------------------------------------------------------------------------------

- Always run `--set-date` or `--advance-time` before recording sales or purchases.
- Use consistent date format: YYYY-MM-DD
- FIFO (First-In First-Out) is used for selling products by expiration date.
- Use the reports to analyze sales and manage restocking.

--------------------------------------------------------------------------------
6. Getting Help
--------------------------------------------------------------------------------

For help with any subcommand:
    python superpy.py buy --help
    python superpy.py sell --help
    python superpy.py report --help

This will show required and optional arguments.

--------------------------------------------------------------------------------
