# Premium Bond Checker

Simple premium bond checker library that is built against [Nsandi](https://www.nsandi.com/) to check if you have won or not.

## Usage

```python
    client = Client()
    result = client.check('your bond number')
    print(f'Winning: {result.has_won()}')
```

## Licence

MIT
