import unittest
from tablipy.core import Tablipy
from io import StringIO
import sys


class TestTablipy(unittest.TestCase):
    def setUp(self):
        self.data = [["John", "30", "New York"], ["Jane", "25", "Los Angeles"]]
        self.col_headers = ["Name", "Age", "Location"]
        self.instance = Tablipy(col_headers=self.col_headers, data=self.data)

    def test_get_row(self):
        row = self.instance.get_row(1)
        self.assertEqual(row, ["Jane", "25", "Los Angeles"])

    def test_get_cell(self):
        cell = self.instance.get_cell(1, 0)
        self.assertEqual(cell, "30")

    def test_set_column(self):
        self.instance.set_column(0, ["Jim", "Jill"])
        new_column = self.instance.get_column(0)
        self.assertEqual(new_column, ["Jim", "Jill"])

    def test_set_row(self):
        self.instance.set_row(1, ["Janet", "28", "Chicago"])
        new_row = self.instance.get_row(1)
        self.assertEqual(new_row, ["Janet", "28", "Chicago"])

    def test_set_cell(self):
        self.instance.set_cell(2, 1, "San Francisco")
        updated_cell = self.instance.get_cell(2, 1)
        self.assertEqual(updated_cell, "San Francisco")

    def test_build_from_data(self):
        new_data = [["Bob", "40", "Boston"]]
        self.instance.build_from_data(new_data)
        new_row = self.instance.get_row(0)
        self.assertEqual(new_row, ["Bob", "40", "Boston"])

    def test_add_column(self):
        self.instance.add_column("Salary", ["50000", "60000"])
        new_column = self.instance.get_column("Salary")
        self.assertEqual(new_column, ["50000", "60000"])

    def test_add_row(self):
        self.instance.add_row(["Sue", "35", "Seattle"])
        new_row = self.instance.get_row(2)
        self.assertEqual(new_row, ["Sue", "35", "Seattle"])


if __name__ == "__main__":
    unittest.main()
