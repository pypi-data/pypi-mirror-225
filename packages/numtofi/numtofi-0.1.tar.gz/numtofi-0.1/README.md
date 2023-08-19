# `numtofi` - Convert numbers to Finnish textual representation

`numtofi` is a Python module that offers functionality to convert integers into their Finnish textual representation. This module also comes with a command-line interface (CLI) tool to quickly get the Finnish representation for any number from the command line.

## Installation

```bash
pip install numtofi
```

## Usage

### As a Python Module

```python
from numtofi import number_to_word

print(number_to_word(45))  # Outputs "neljäkymmentäviisi"
```

### Command-Line Interface (CLI)

After installation, you can use the `numtofi` command directly from your terminal:

```bash
$ numtofi 45
neljäkymmentäviisi
```

```bash
$ numtofi 5000000 --space
viisi miljoonaa
```

## Parameters

- `number_to_word(n, space=False)`:
  - `n (int)`: The number to convert.
  - `space (bool)`: If `True`, add a space between words. Default is `False`.

## Testing

Tests are provided in the `tests` directory. To run the tests:

1. Navigate to the project root directory.
2. Run:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please make sure to update tests as appropriate when proposing changes.

## License

[MIT](LICENSE)
