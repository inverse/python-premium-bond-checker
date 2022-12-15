import sys

from client import Client

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must provide a holder number to check ")
        exit(1)

    print(f"Checking {sys.argv[1]}")
    client = Client()
    result = client.check(sys.argv[1])
    print(f"Winning: {result.has_won()}")
