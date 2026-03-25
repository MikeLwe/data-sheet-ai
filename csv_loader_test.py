"""
Tests for csv_loader Module
"""

import csv_loader
from unittest.mock import patch
import pandas

def test_read_csv_1():
    """No Title Input & Read CSV Test"""
    correct_data = pandas.DataFrame({
        "First Name": ["Alice", "Bryce", "Carlos"],
        "Last Name": ["A", "B", "C"],
        "School E-mail": ["alice@bu.edu", "bryce@bu.edu", "carl@bu.edu"]
    })
    with patch("builtins.input", side_effect=["datatables/test1.csv", ""]):
        test_data, test_title = csv_loader.read_csv()
        assert correct_data.equals(test_data)
        assert test_title == "test1"

def test_read_csv_2():
    """Title Input & Read CSV Test"""
    correct_data = pandas.DataFrame({
        "First Name": ["Alice"],
        "Unique ID": ["12563U"],
        "ID": [1234567]
    })
    with patch("builtins.input", side_effect=["datatables/test2.csv", "Custom Table"]):
        test_data, test_title = csv_loader.read_csv()
        assert correct_data.equals(test_data)
        assert test_title == "Custom Table"
