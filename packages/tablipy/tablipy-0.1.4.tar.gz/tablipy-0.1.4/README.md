# Tablipy

Tablipy is a Python library for working with tabular data. It provides a simple and intuitive way to create, manipulate, and print tabular data structures.

## Installation

You can install Tablipy using pip:

```bash
pip install tablipy
```

## Usage

Here's a basic example of how to use Tablipy to create a table, add data, and print it:

```python
from tablipy.core import Tablipy

# Create an instance of Tablipy
table = Tablipy(col_headers=['Name', 'Age', 'Location'])

# Add data to the table
table.add_row(['John', '30', 'New York'])
table.add_row(['Jane', '25', 'Los Angeles'])

# Print the table
table.print()
```

For more detailed information and examples, check the [documentation](https://github.com/mirolaukka/tablipy/blob/main/documentation.md) or explore the examples in the `tests` directory.

## Features

- Create tables with specified column headers.
- Add data to the table as rows.
- Get specific columns, rows, or cells from the table.
- Set values of columns, rows, or cells.
- Print tables in a neat tabular format.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests on the [GitHub repository](https://github.com/mirolaukka/tablipy).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.