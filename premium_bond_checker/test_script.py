import sys
import os

from premium_bond_checker.client import Client

if __name__ == "__main__":
    premium_bond_number = os.environ.get('PREMIUM_BOND_NUMBER')

    if len(sys.argv) == 2:
        premium_bond_number = sys.argv[1]

    if premium_bond_number is None:
        print("You must provide a holder number to check")
        exit(1)

    print(f"Checking {premium_bond_number}")
    client = Client()
    result = client.check(premium_bond_number)
    print(f"Winning: {result.has_won()}")
