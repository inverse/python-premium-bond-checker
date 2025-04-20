# Premium Bond Checker

![CI](https://github.com/inverse/python-premium-bond-checker/workflows/CI/badge.svg)
[![PyPI version](https://badge.fury.io/py/premium-bond-checker.svg)](https://badge.fury.io/py/premium-bond-checker)
![PyPI downloads](https://img.shields.io/pypi/dm/premium-bond-checker?label=pypi%20downloads)
[![License](https://img.shields.io/github/license/inverse/cert-host-scraper.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/github/inverse/python-premium-bond-checker/graph/badge.svg?token=3IM22FJIJM)](https://codecov.io/github/inverse/python-premium-bond-checker)


Simple premium bond checker library that is built against [Nsandi](https://www.nsandi.com/).

## Usage

### Check next draw date

You can check the next draw date, which is calculated from the first working day of the month.

```python
from premium_bond_checker.client import Client

premium_bond_number = 'your bond number'

client = Client()

# Getting next draw date
next_draw = client.next_draw()
print(f"Next draw: {next_draw}")
```

### Check results

Results can be checked either granular or on all data points.

```python
from premium_bond_checker.client import Client

premium_bond_number = 'your bond number'

client = Client()

# Check if you've won
result = client.check(premium_bond_number)
print(f"Winning: {result.has_won()}")

# More granular breakdown
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
```
## License

MIT
