"""
Tests for schema_manager Module
"""

import csv_loader
import schema_manager
from unittest.mock import patch

def test_read_csv_1():
    """Column Schema String Test on test1.csv"""
    # correct_data = pandas.DataFrame({
    #     "First Name": ["Alice", "Bryce", "Carlos"],
    #     "Last Name": ["A", "B", "C"],
    #     "School E-mail": ["alice@bu.edu", "bryce@bu.edu", "carl@bu.edu"]
    # })
    correct_string = '"First Name" TEXT, "Last Name" TEXT, "School E-mail" TEXT'
    with patch("builtins.input", side_effect=["datatables/test1.csv", ""]):
        test_data, = csv_loader.read_csv()
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string

def test_read_csv_2():
    """Title Input & Read CSV Test"""
    # correct_data = pandas.DataFrame({
    #     "First Name": ["Alice"],
    #     "Unique ID": ["12563U"],
    #     "ID": [1234567]
    # })
    correct_string = '"First Name" TEXT, "Unique ID" TEXT, "ID" INTEGER'
    with patch("builtins.input", side_effect=["datatables/test2.csv", "Custom Table"]):
        test_data, = csv_loader.read_csv()
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string
