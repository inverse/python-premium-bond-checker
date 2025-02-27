import os
import sys

from premium_bond_checker.client import Client

if __name__ == "__main__":
    premium_bond_number = os.environ.get("PREMIUM_BOND_NUMBER")

    if len(sys.argv) == 2:
        premium_bond_number = sys.argv[1]

    if premium_bond_number is None:
        print("You must provide a holder number to check")
        exit(1)

    print(f"Checking {premium_bond_number}")
    client = Client()

    if not client.is_holder_number_valid(premium_bond_number):
        print("Invalid holder number given")
        exit(1)

    next_draw = client.next_draw()
    print(f"Next draw: {next_draw}")

    result = client.check(premium_bond_number)
    print(f"Winning: {result.has_won()}")

    result_this_month = client.check_this_month(premium_bond_number)
    print(f"This Month Winning: {result_this_month.won}")
    print(f"This Month Header: {result_this_month.header}")
    print(f"This Month Tagline: {result_this_month.tagline}")

    result_last_six_months = client.check_last_six_months(premium_bond_number)
    print(f"This Month Winning: {result_last_six_months.won}")
    print(f"This Month Header: {result_last_six_months.header}")
    print(f"This Month Tagline: {result_last_six_months.tagline}")

    result_check_unclaimed = client.check_unclaimed(premium_bond_number)
    print(f"This Month Winning: {result_check_unclaimed.won}")
    print(f"This Month Header: {result_check_unclaimed.header}")
    print(f"This Month Tagline: {result_check_unclaimed.tagline}")
