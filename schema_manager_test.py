"""
Tests for schema_manager Module
"""

import csv_loader
import schema_manager
from unittest.mock import patch
import sqlite3 as sql

#REMEMBER TO CHANGE THIS LATER
database = 'test_database.db'

def test_col_schema_1():
    """Column Schema String Test on test1.csv"""
    correct_string = '"Row ID" INTEGER, "First Name" TEXT, "Last Name" TEXT, "School E-mail" TEXT'
    with patch("builtins.input", side_effect=[""]):
        test_data, _ = csv_loader.read_csv("datatables/test1.csv")
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string

def test_col_schema_2():
    """Column Schema String Test on test2.csv"""
    correct_string = '"Row ID" INTEGER, "First Name" TEXT, "Unique ID" TEXT, "ID" INTEGER'
    with patch("builtins.input", side_effect=["Custom Table"]):
        test_data, _ = csv_loader.read_csv("datatables/test2.csv")
        test_string = schema_manager.col_schema(test_data)
        assert correct_string == test_string

# def test_create_table_1():
#     """Create SQL Table Test on test1.csv"""
#     correct_string = '"Row_ID" INTEGER, "First Name" TEXT, "Last Name" TEXT, "School E-mail" TEXT'
#     with patch("builtins.input", side_effect=[""]):
#         test_content, test_title = csv_loader.read_csv("datatables/test1.csv")
#         schema_manager.create_table(test_content, test_title, database)
#         assert correct_string == test_string

def test_table_checker_1():
    """Test table_checker by creating a table and checking it"""
    with patch("builtins.input", side_effect=["", "4"]):
        test_content, test_title = csv_loader.read_csv("datatables/test1.csv")
        schema_manager.create_table(test_content, test_title, database)
        test_connection = sql.connect(database)
        test_cursor = test_connection.cursor()
        test_result = schema_manager.table_checker(test_cursor, test_title)
        test_connection.commit()
        test_connection.close()
        assert test_result

def test_table_checker_2():
    """Test table_checker 2"""
    with patch("builtins.input", side_effect=["Custom Table"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database)
        test_connection = sql.connect(database)
        test_cursor = test_connection.cursor()
        test_result = schema_manager.table_checker(test_cursor, test_title)
        test_connection.commit()
        test_connection.close()
        assert test_result

def test_get_schema():
    """Table Schema Prompt String Test on test_database.db"""
    correct_string = """ - "test1" ("Row Id", ""First Name", "Last Name", "School E-mail") - "Custom Table" ("Row Id", "First Name", "Unique ID", "ID")"""
    with patch("builtins.input", side_effect=[""]):
        test_string = schema_manager.get_schema(database)
        assert correct_string == test_string

# def test_get_schema_2():
#     """Table Schema Prompt String Test on test2.csv"""
#     correct_string = '"Custom Table" - ("First Name", "Unique ID", "ID")'
#     with patch("builtins.input", side_effect=["Custom Table"]):
#         test_data, _ = csv_loader.read_csv("datatables/test2.csv")
#         test_string = schema_manager.get_schema(database)
#         assert correct_string == test_string