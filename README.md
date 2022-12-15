# Premium Bond Checker

Simple premium bond checker library that is built against [Nsandi](https://www.nsandi.com/).

## Usage

```python
from premium_bond_checker.client import Client

client = Client()
result = client.check('your bond number')
print(f'Winning: {result.has_won()}')
```

## Licence

MIT
