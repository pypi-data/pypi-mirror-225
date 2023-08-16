from typing import Union, List


class Tablipy:
    def __init__(self, col_headers: List[str] = [], data: List[List[str]] = None):
        """
        Initialize a Tablipy instance with optional column headers and pre-existing data.

        Parameters:
        - col_headers (List[str], optional): List of column headers. Default is an empty list.
        - data (List[List[str]], optional): Pre-existing data to initialize the table. Default is None.

        Attributes:
        - col_headers (List[str]): List of column headers.
        - cols (List[int]): List of column indexes corresponding to the column headers.
        - rows (List[List[str]]): List of rows, where each row is represented as a list of cell values.
        - table (List[list]): A composite list containing col_headers and rows.

        If 'data' is provided, the table is populated with the data using the 'build_from_data' method.

        Example usage:
        ```
        instance = Tablipy(col_headers=['Name', 'Age', 'Location'], data=[['John', '30', 'New York'], ['Jane', '25', 'Los Angeles']])
        ```
        """

        self.col_headers = col_headers
        self.cols = [n for n in range(len(col_headers))]
        self.rows = []
        self.table = [self.col_headers, self.rows]
        if data:
            self.build_from_data(data)

    def get_column(self, col: Union[str, int]):
        """
        Retrieve the values of a column based on either the column index or header name.

        Parameters:
        - col (Union[str, int]): The column index or header name to retrieve the values from.

        Returns:
        - list: The data of the column at the specified index or header.

        Raises:
        - ValueError: If the provided column index or header does not exist in the dataset.
        - IndexError: If the provided column index is out of range.
        """

        if isinstance(col, str):
            return self._get_column_by_index(self._get_column_by_header(col))
        if isinstance(col, int):
            return self._get_column_by_index(col)

    def _get_column_by_header(self, header: str):
        """
        Return the index of the column based on the given header

        Parameters:
        - header (str): The header name to search for

        Returns:
        - int: The index of the column

        Raises:
        - ValueError: If the provided header does not exist in the dataset
        """

        try:
            index = self.col_headers.index(header)
            return index
        except ValueError:
            raise ValueError(f"Header '{header}' not found in the table")

    def _get_column_by_index(self, column_index: int):
        """
        Retrieve a column by its index.

        Parameters:
        - column_index (int): The index of the column to retrieve.

        Returns:
        - list: The data of the column at the specified index.

        Raises:
        - IndexError: If the column_index is out of range.
        """

        if 0 <= column_index < len(self.col_headers):
            return [row[column_index] for row in self.rows]
        else:
            raise IndexError(f"Column index {column_index} is out of range.")

    def get_row(self, row_index: int):
        """
        Retrieve a row by its index.

        Parameters:
        - row_index (int): The index of the row to retrieve.

        Returns:
        - list: The data of the row at the specified index.

        Raises:
        - IndexError: If the row_index is out of range.
        """

        if 0 <= row_index < len(self.rows):
            return self.rows[row_index]
        else:
            raise IndexError(f"Row index {row_index} is out of range.")

    def get_cell(self, column_index: Union[int, str], row_index: int):
        """
        Retrieve a cell by its column and row indexes.

        Parameters:
        - column_index (Union[int, str]): The index of the column or header name.
        - row_index (int): The index of the row.

        Returns:
        - str: The value of the cell at the specified column and row indexes.

        Raises:
        - IndexError: If either the column_index or row_index is out of range.
        """

        if isinstance(column_index, str):
            column_index = self._get_column_by_header(column_index)

        if 0 <= column_index < len(self.col_headers) and 0 <= row_index < len(
            self.rows
        ):
            return self.rows[row_index][column_index]
        else:
            raise IndexError(
                f"Column index {column_index} or row index {row_index} is out of range."
            )

    def set_column(self, column_index: int, data: List[str]):
        """
        Set the values of a column at the specified index with the provided data.

        Parameters:
        - column_index (int): Index of the column to set.
        - data (List[str]): List of values to set in the column.
        """
        if not (0 <= column_index < len(self.col_headers)):
            raise IndexError(f"Column index {column_index} is out of range.")

        if len(data) != len(self.rows):
            raise ValueError(
                "Number of data elements doesn't match the number of rows."
            )

        for i, value in enumerate(data):
            self.rows[i][column_index] = value

    def set_row(self, row_index: int, data: List[str]):
        """
        Set the values of a row at the specified index with the provided data.

        Parameters:
        - row_index (int): Index of the row to set.
        - data (List[str]): List of values to set in the row.
        """
        if not (0 <= row_index < len(self.rows)):
            raise IndexError(f"Row index {row_index} is out of range.")

        if len(data) != len(self.col_headers):
            raise ValueError(
                "Number of data elements doesn't match the number of columns."
            )

        self.rows[row_index] = data

    def set_cell(self, column_index: int, row_index: int, data: str):
        """
        Set the value of a specific cell at the specified column and row indexes.

        Parameters:
        - column_index (int): Index of the column.
        - row_index (int): Index of the row.
        - data (str): Value to set in the cell.
        """
        if not (0 <= column_index < len(self.col_headers)) or not (
            0 <= row_index < len(self.rows)
        ):
            raise IndexError(
                f"Column index {column_index} or row index {row_index} is out of range."
            )

        self.rows[row_index][column_index] = data

    def print(self):
        """
        Pretty print the table in a tabular format.
        """
        col_widths = [
            max(len(header), max(len(str(row[i])) for row in self.rows))
            for i, header in enumerate(self.col_headers)
        ]

        header_line = "| ".join(
            f"{header:<{col_widths[i]}}" for i, header in enumerate(self.col_headers)
        )
        divider_line = "+-".join("-" * width for width in col_widths)

        print("  " + divider_line + "  ")
        print("| " + header_line + " |")
        print("| " + divider_line + " |")

        for row in self.rows:
            row_line = "| ".join(
                f"{cell:<{col_widths[i]}}" for i, cell in enumerate(row)
            )
            print("| " + row_line + " |")
        print("  " + divider_line + "  ")

    def build_from_data(self, data: List[List[str]], col_headers: List[str] = None):
        """
        Populate the table with data provided in the form of a list of rows.

        Parameters:
        - data (List[List[str]]): List of rows to populate the table with.
        - col_headers (List[str], optional): List of column headers. If not provided, existing col_headers are used.
        """
        if not col_headers and not self.col_headers:
            raise ValueError("Cannot build from data without column headers.")

        if col_headers:
            self.col_headers = col_headers

        if len(self.col_headers) != len(data[0]):
            raise ValueError(
                "Number of columns in data doesn't match the number of column headers."
            )

        self.rows = data

    def add_column(self, header: str, data: List[str] = None):
        """
        Add a new column to the table.

        Parameters:
        - header (str): The header name of the new column.
        - data (List[str], optional): List of values to populate the new column. Default is None.
        """
        if header in self.col_headers:
            raise ValueError(f"Column with header '{header}' already exists.")

        if data and len(data) != len(self.rows):
            raise ValueError(
                "Number of data elements doesn't match the number of rows."
            )

        self.col_headers.append(header)
        self.cols.append(len(self.col_headers) - 1)  # Add the new column index

        if data:
            for i, value in enumerate(data):
                self.rows[i].append(value)

    def add_row(self, data: List[Union[str, int]]):
        """
        Add a new row to the table.

        Parameters:
        - data (List[Union[str, int]]): List of values to populate the new row.
        """
        if len(data) != len(self.col_headers):
            raise ValueError(
                "Number of data elements doesn't match the number of columns."
            )

        self.rows.append(data)
