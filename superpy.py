# Imports
import argparse
import csv
import re
import os
from datetime import datetime, date, timedelta
from collections import defaultdict
from argparse import RawTextHelpFormatter
from rich.console import Console
from rich.panel import Panel

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

# Sets the current date used by the system if the format is valid
def set_date(date):
    # Open the file storing the current date
    with open("data/current_time.txt", "r+") as f:
        # Check if the date format is valid (yyyy-mm-dd)
        if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', date):
            new_date = datetime.strptime(date, "%Y-%m-%d").date()
            # Overwrite the file with the new date
            f.seek(0)
            f.write(str(new_date))
            f.truncate()
            print("OK")
        else:
            print("Date should be in yyyy-mm-dd format!")
    
# Advances the current date by a given number of days; creates date file if it doesn't exist
def advance_time(days):
    # Open the file containing the current date
    with open("data/current_time.txt", "r+") as f:
        content = f.read().strip()

        if content == "":
            # If no date is set, default to today's date
            current_date = str(datetime.now().date())
            f.seek(0)
            f.write(current_date)
            f.truncate()
            print("OK")
        else:
            # Parse the current date and add the specified number of days
            set_date = datetime.strptime(content, "%Y-%m-%d").date()
            new_date = set_date + timedelta(days=days)
            f.seek(0)
            f.write(str(new_date))
            f.truncate()
            print("OK")
    
# Records a product purchase in `bought.csv`, updates or creates the product in inventory
def order_product(args):
    # Count existing rows in bought.csv to determine the next ID
    with open('data/bought.csv', 'r', newline='') as bought_csv:
        csvreader = csv.reader(bought_csv, delimiter=',', quotechar='"')
        next(csvreader)
        current_bought_rows = sum(1 for _ in csvreader)

    # Append a new row to bought.csv for the product
    with open('data/bought.csv', 'a', newline='') as bought_csv:
        csvwriter = csv.writer(bought_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        buy_date = datetime.now().date()
        csvwriter.writerow([current_bought_rows + 1, args.product_name, args.count if args.count is not None else 1, buy_date, args.price, args.expiration_date])

    updated = False
    updated_inventory = []
    
    # Check if product already exists in inventory to update it
    with open('data/inventory.csv', 'r', newline='') as inventory_csv:
        csvreader = csv.reader(inventory_csv, delimiter=',', quotechar='"')
        header = next(csvreader)
        for row in csvreader:
            if row[1] == args.product_name:
                row[3] = str(int(row[3]) + args.count)
                # Choose earliest expiration date if multiple entries exist
                d1 = datetime.strptime(args.expiration_date, "%Y-%m-%d").date()
                d2 = datetime.strptime(row[4], "%Y-%m-%d").date()
                if(d1 < d2):
                    row[4] = d1
                row[2] = args.price
                updated = True
            updated_inventory.append(row)
    
    current_inventory_rows = len(updated_inventory)

    if updated:
        # Overwrite inventory file with updated values
        with open('data/inventory.csv', 'w', newline='') as inventory_csv:
            csvwriter = csv.writer(inventory_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            csvwriter.writerows(updated_inventory)
        pass
    else:
        # Append new product to inventory if it wasn't found
        with open('data/inventory.csv', 'a', newline='') as inventory_csv:
            csvwriter = csv.writer(inventory_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            buy_date = datetime.now().date()
            csvwriter.writerow([current_inventory_rows + 1, args.product_name, args.price, args.count if args.count is not None else 1, args.expiration_date])
    
    print(f"Ordered {args.count} unit(s) of {args.product_name}.")

# Generates inventory, revenue, or profit reports based on date filters (now, yesterday, or custom date)
def report(args):
    # Read current date and calculate yesterday's date 
    with open('data/current_time.txt', 'r') as f:
        current_date = f.read()
        yesterday = datetime.strptime(current_date, "%Y-%m-%d").date() + timedelta(days=-1)

    # Handle inventory report
    if args.type is not None and args.type == 'inventory':
        with open('data/inventory.csv', 'r', newline='') as inventory_csv:
            csvreader = csv.reader(inventory_csv, delimiter=',', quotechar='"')
            header = next(csvreader)
            print(header)
            for row in csvreader:
                # Filter based on now, yesterday, or a specific date
                if args.now is True:
                    if current_date in row:
                        print(row)
                elif args.yesterday is True:
                    if str(yesterday) in row:
                        print(row)
                elif args.date:
                    if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', args.date):
                        if args.date in row:
                            print(row)
                    else:
                        print("Date should be in yyyy-mm-dd format!")
                        return
                else:
                    print(row)

    # Handle revenue report
    if args.type is not None and args.type == 'revenue':
        with open('data/sold.csv', 'r', newline='') as sold_csv:
            csvreader = csv.reader(sold_csv, delimiter=',', quotechar='"')
            next(csvreader)
            revenue = 0
            for row in csvreader:
                row_revenue = 0
                # Calculate revenue based on date filters
                if args.now is True:
                    if current_date in row:
                        row_revenue = float(row[4]) * int(row[5])
                elif args.yesterday is True:
                    if str(yesterday) in row:
                        row_revenue = float(row[4]) * int(row[5])
                elif args.date:
                    if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', args.date):
                        if args.date in row:
                            row_revenue = float(row[4]) * int(row[5])
                    else:
                        print("Date should be in yyyy-mm-dd format!")
                        return
                else:
                    row_revenue = float(row[4]) * int(row[5])
                revenue += row_revenue
            # Output revenue summary
            if args.now is True:
                if current_date in row:
                    print(f"Today's revenue so far: {revenue}")
            elif args.yesterday is True:
                print(f"Yesterday's revenue: {revenue}")
            elif args.date:
                print(f"Revenue from {args.date}: {revenue}")
            else:
                print(f"Total revenue: {revenue}")

    # Handle profit report
    if args.type is not None and args.type == 'profit':
        profit = 0
        products_revenue = 0
        products_cost = 0

        # Calculate revenue
        with open('data/sold.csv', 'r', newline='') as sold_csv:
            csvreader = csv.reader(sold_csv, delimiter=',', quotechar='"')
            next(csvreader)
            for row in csvreader:
                row_revenue = 0
                if args.now is True:
                    if current_date in row:
                        row_revenue = float(row[4]) * int(row[5])
                elif args.yesterday is True:
                    if str(yesterday) in row:
                        row_revenue = float(row[4]) * int(row[5])
                elif args.date:
                    if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', args.date):
                        if args.date in row:
                            row_revenue = float(row[4]) * int(row[5])
                    else:
                        print("Date should be in yyyy-mm-dd format!")
                        return
                else:
                    row_revenue = float(row[4]) * int(row[5])
                products_revenue += row_revenue
                
        # Calculate costs
        with open('data/bought.csv', 'r', newline='') as bought_csv:
            csvreader = csv.reader(bought_csv, delimiter=',', quotechar='"')
            next(csvreader)
            for row in csvreader:
                row_cost = 0
                if args.now is True:
                    if current_date in row:
                        row_cost = int(row[2]) * float(row[4])
                elif args.yesterday is True:
                    if str(yesterday) in row:
                        row_cost = int(row[2]) * float(row[4])
                elif args.date:
                    if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', args.date):
                        if args.date in row:
                            row_cost = int(row[2]) * float(row[4])
                    else:
                        print("Date should be in yyyy-mm-dd format!")
                else:
                    row_cost = int(row[2]) * float(row[4])
                products_cost += row_cost  
        
        # Output final profit
        profit = products_revenue - products_cost
        if args.now is True:
            if current_date in row:
                print(f"Today's profit so far: {profit}")
        elif args.yesterday is True:
            print(f"Yesterday's profit: {profit}")
        elif args.date:
            print(f"Profit from {args.date}: {profit}")
        else:
            print(f"Total profit: {profit}")

# Records a sale of a product, updates `sold.csv`, and updates inventory accordingly
def sell_product(args):
    sell_date = datetime.today().strftime("%Y-%m-%d")
    product_name = args.product_name
    quantity_to_sell = args.count

    # Load all purchases of the specified product
    with open('data/bought.csv', 'r', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        bought_header = next(bought_reader)
        bought_rows = [row for row in bought_reader if row[1] == product_name]

    sold_path = 'data/sold.csv'
    sold_counts = defaultdict(int)

    # Tally how many units of each batch have already been sold
    if os.path.exists(sold_path):
        with open(sold_path, 'r', newline='') as sold_file:
            sold_reader = csv.reader(sold_file)
            sold_header = next(sold_reader)
            for row in sold_reader:
                sold_counts[row[1]] += int(row[5])

    available_batches = []

    # Calculate how many units are available for sale per batch
    for row in bought_rows:
        bought_id = row[0]
        original_count = int(row[2])
        sold_count = sold_counts[bought_id]
        available = original_count - sold_count

        if available > 0:
            available_batches.append({
                'bought_id': bought_id,
                'product_name': row[1],
                'sell_price': row[4],
                'expiration_date': row[5],
                'available': available
            })

    # Sort batches by earliest expiration date (FIFO approach)
    available_batches.sort(key=lambda x: datetime.strptime(x['expiration_date'], "%Y-%m-%d"))

    remaining = quantity_to_sell
    sold_rows = []

    # Sell from oldest available batches first
    for batch in available_batches:
        if remaining <= 0:
            break

        sell_count = min(remaining, batch['available'])
        remaining -= sell_count

        sold_rows.append([
            '',  # Placeholder for ID
            batch['bought_id'],
            product_name,
            sell_date,
            batch['sell_price'],
            sell_count,
            batch['expiration_date']
        ])

    # Not enough stock to fulfill order
    if remaining > 0:
        print(f"Not enough stock to sell {quantity_to_sell} {product_name}(s).")
        return

    sold_exists = os.path.isfile(sold_path)

    # Determine last used ID in `sold.csv`
    last_id = 0
    if sold_exists:
        with open(sold_path, 'r', newline='') as sold_file:
            sold_reader = csv.reader(sold_file)
            next(sold_reader)
            for row in sold_reader:
                last_id = max(last_id, int(row[0]))

    # Write new sales to `sold.csv`
    with open(sold_path, 'a', newline='') as sold_file:
        sold_writer = csv.writer(sold_file)
        if not sold_exists:
            sold_writer.writerow(['id','bought_id','product_name','sell_date','sell_price','count','expiration_date'])

        for i, row in enumerate(sold_rows, start=1):
            row[0] = last_id + i  # Assign new ID
            sold_writer.writerow(row)

    # Update inventory stock and earliest expiration date
    with open('data/inventory.csv', 'r', newline='') as inv_file:
        inv_reader = csv.reader(inv_file)
        inv_header = next(inv_reader)
        inv_rows = list(inv_reader)

    new_inv_rows = []

    for row in inv_rows:
        if row[1] == product_name:
            current_stock = int(row[3])
            new_stock = current_stock - quantity_to_sell

            exp_dates = []
            for batch in available_batches:
                sold_for_batch = next((r for r in sold_rows if r[1] == batch['bought_id']), None)
                sold_amount = sold_for_batch[5] if sold_for_batch else 0
                remaining_after_sale = batch['available'] - sold_amount
                if remaining_after_sale > 0:
                    exp_dates.append(datetime.strptime(batch['expiration_date'], "%Y-%m-%d"))
            
            # Set next earliest expiration date if stock remains
            new_exp_date = min(exp_dates).strftime("%Y-%m-%d") if exp_dates else ''

            row[3] = str(new_stock)
            row[4] = new_exp_date

        new_inv_rows.append(row)

    # Overwrite inventory with updated stock
    with open('data/inventory.csv', 'w', newline='') as inv_file:
        inv_writer = csv.writer(inv_file)
        inv_writer.writerow(inv_header)
        inv_writer.writerows(new_inv_rows)

    print(f"Successfully sold {quantity_to_sell} units of {product_name}.")

# Executes the subcommand function if one was passed via the parser
def main():
    if hasattr(args, 'func'):
        args.func(args)

console = Console()

epilog_text = """[bold underline yellow]buy:[/bold underline yellow]
  [cyan]--product-name NAME[/cyan]        Name of the product to purchase (required)
  [cyan]--price PRICE[/cyan]              Price per unit of the product (required)
  [cyan]--count COUNT[/cyan]              Quantity of the product to purchase (default: 1)
  [cyan]--expiration-date DATE[/cyan]     Expiration date of the product (yyyy-mm-dd) (required)

[bold underline yellow]sell:[/bold underline yellow]
  [cyan]--product-name NAME[/cyan]        Name of the product to sell (required)
  [cyan]--count COUNT[/cyan]              Quantity of the product to sell (required)

[bold underline yellow]report:[/bold underline yellow]
  [cyan]type[/cyan]                       Type of report: 'inventory', 'revenue', or 'profit' (optional)
  [cyan]--now[/cyan]                      Report for the current date
  [cyan]--yesterday[/cyan]                Report for the previous day
  [cyan]--date YYYY-MM-DD[/cyan]          Report for a specific date

[bold]Note:[/bold]
  Use 'python superpy.py <command> --help' to view detailed help for each subcommand."""


parser = argparse.ArgumentParser(    
    prog="superpy",
    description="superpy: a CLI tool to manage inventory, sales, and reports for a simple store.",
    add_help=False)

parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
parser.add_argument("--advance-time", type=int, help="Advance the current date by a number of days")
parser.add_argument("--set-date", type=str, help="Set the current date manually in yyyy-mm-dd format")

subparsers = parser.add_subparsers(title="commands", description="Available subcommands. Use 'python superpy.py <command> --help' for more details.", dest="command", required=False)

parser_order_product = subparsers.add_parser("buy", help="Record the purchase of a product")
parser_order_product.add_argument("--product-name", required=True, help="Name of the product to purchase")
parser_order_product.add_argument("--price", type=float, required=True, help="Price per unit of the product")
parser_order_product.add_argument("--count", type=int, required=False, help="Quantity of the product to purchase (default: 1)")
parser_order_product.add_argument("--expiration-date", required=True, help="Expiration date of the product (yyyy-mm-dd)")
parser_order_product.set_defaults(func=order_product)

parser_order_product = subparsers.add_parser("sell", help="Record the sale of a product")
parser_order_product.add_argument("--product-name", required=True, help="Name of the product to sell")
parser_order_product.add_argument("--count", type=int, required=True, help="Quantity of the product to sell")
parser_order_product.set_defaults(func=sell_product)

parser_report = subparsers.add_parser("report", help="Generate inventory, revenue, or profit reports")
parser_report.add_argument("type", nargs='?', choices=["inventory", "revenue", "profit"], help="Type of report: 'inventory', 'revenue', or 'profit'")
parser_report.add_argument("--now", action="store_true", help="Report for the current date")
parser_report.add_argument("--yesterday", action="store_true", help="Report for the previous day")
parser_report.add_argument("--date", type=str,required=False, help="Report for a specific date (yyyy-mm-dd)")
parser_report.set_defaults(func=report)

args = parser.parse_args()

if args.advance_time is not None:
    advance_time(args.advance_time)

if args.set_date is not None:
    set_date(args.set_date)

if args.help:
    console.print(f"[bold green]Usage:[/bold green] python superpy.py [OPTIONS]")
    console.print(Panel(epilog_text, title="[bold magenta]superpy[/bold magenta] Help", expand=False))
    exit()


if __name__ == "__main__":
    main()