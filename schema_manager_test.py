"""
Tests for schema_manager Module
"""

import csv_loader
import schema_manager
from unittest.mock import patch

def test_col_schema_1():
    """Column Schema String Test on test1.csv"""
    correct_string = '"First Name" TEXT, "Last Name" TEXT, "School E-mail" TEXT'
    with patch("builtins.input", side_effect=["datatables/test1.csv", ""]):
        test_data, _ = csv_loader.read_csv()
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string

def test_col_schema_2():
    """Column Schema String Test on test2.csv"""
    correct_string = '"First Name" TEXT, "Unique ID" TEXT, "ID" INTEGER'
    with patch("builtins.input", side_effect=["datatables/test2.csv", "Custom Table"]):
        test_data, _ = csv_loader.read_csv()
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string

def test_create_table_1():
    """Create SQL Table Test on test1.csv"""
    correct_string = '"First Name" TEXT, "Unique ID" TEXT, "ID" INTEGER'
    with patch("builtins.input", side_effect=["datatables/test1.csv", "Test Table1"]):
        test_data, _ = csv_loader.read_csv()
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string