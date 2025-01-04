# Premium Bond Checker

![CI](https://github.com/inverse/python-premium-bond-checker/workflows/CI/badge.svg)
[![PyPI version](https://badge.fury.io/py/premium-bond-checker.svg)](https://badge.fury.io/py/premium-bond-checker)
![PyPI downloads](https://img.shields.io/pypi/dm/premium-bond-checker?label=pypi%20downloads)
[![License](https://img.shields.io/github/license/inverse/cert-host-scraper.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/github/inverse/python-premium-bond-checker/graph/badge.svg?token=3IM22FJIJM)](https://codecov.io/github/inverse/python-premium-bond-checker)


Simple premium bond checker library that is built against [Nsandi](https://www.nsandi.com/).

## Usage

```python
from premium_bond_checker.client import Client

client = Client()
result = client.check('your bond number')
print(f'Winning: {result.has_won()}')
```

## License

MIT
