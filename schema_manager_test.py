"""
Tests for schema_manager Module
"""

import csv_loader
import schema_manager
from unittest.mock import patch
import sqlite3 as sql

database = 'test_database.db'
backup_data = 'test_backup.db'
backup_key = 'test_key.db'

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

def test_table_checker_1():
    """Test table_checker by creating a table and checking it"""
    with patch("builtins.input", side_effect=["", "4"]):
        test_content, test_title = csv_loader.read_csv("datatables/test1.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        test_connection = sql.connect(database)
        test_cursor = test_connection.cursor()
        test_result = schema_manager.table_checker(test_cursor, test_title)
        test_connection.commit()
        test_connection.close()
        assert test_result

def test_table_checker_2():
    """Test table_checker 2"""
    with patch("builtins.input", side_effect=["Custom Table", "4"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        test_connection = sql.connect(database)
        test_cursor = test_connection.cursor()
        test_result = schema_manager.table_checker(test_cursor, test_title)
        test_connection.commit()
        test_connection.close()
        assert test_result

def test_get_schema():
    """Table Schema Prompt String Test on test_database.db"""
    correct_string = """ - "test1" ("Row ID", "First Name", "Last Name", "School E-mail") - "Custom Table" ("Row ID", "First Name", "Unique ID", "ID")"""
    test_string = schema_manager.get_schema(database)
    assert correct_string == test_string

def test_get_data_1():
    """Table Display String Test on test1.csv"""
    correct_string = """+----------+--------------+-------------+-----------------+
|   Row ID | First Name   | Last Name   | School E-mail   |
+==========+==============+=============+=================+
|        0 | Alice        | A           | alice@bu.edu    |
+----------+--------------+-------------+-----------------+
|        1 | Bryce        | B           | bryce@bu.edu    |
+----------+--------------+-------------+-----------------+
|        2 | Carlos       | C           | carl@bu.edu     |
+----------+--------------+-------------+-----------------+"""
    test_query = 'select * from "test1"'
    test_string = schema_manager.get_data(test_query, database)
    assert correct_string == test_string

def test_get_data_2():
    """Table Display String Test on test1.csv"""
    correct_string = """+----------+--------------+-------------+-----------------+
|   Row ID | First Name   | Last Name   | School E-mail   |
+==========+==============+=============+=================+
|        0 | Alice        | A           | alice@bu.edu    |
+----------+--------------+-------------+-----------------+
|        1 | Bryce        | B           | bryce@bu.edu    |
+----------+--------------+-------------+-----------------+"""
    test_query = 'select * from "test1" where "Row ID" < 2'
    test_string = schema_manager.get_data(test_query, database)
    assert correct_string == test_string

def test_get_data_3():
    """Table Display String Test on test2.csv"""
    correct_string = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
    test_query = 'select * from "Custom Table"'
    test_string = schema_manager.get_data(test_query, database)
    assert correct_string == test_string

def test_get_data_4():
    """Table Display String Test on test2.csv"""
    correct_string = """+----------+--------------+-------------+------+
| Row ID   | First Name   | Unique ID   | ID   |
+==========+==============+=============+======+
+----------+--------------+-------------+------+"""
    test_query = 'select * from "Custom Table" where "ID" < 2'
    test_string = schema_manager.get_data(test_query, database)
    assert correct_string == test_string

def test_table_append_rows():
    """Test create_table user options"""
    with patch("builtins.input", side_effect=["Custom Table", "1"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        correct_string = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+
|        1 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query = 'select * from "Custom Table"'
        test_string = schema_manager.get_data(test_query, database)
        assert correct_string == test_string


def test_table_new_entry():
    """Test create_table user options"""
    with patch("builtins.input", side_effect=["Custom Table", "2", "New Custom Table"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        correct_string = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query = 'select * from "New Custom Table"'
        test_string = schema_manager.get_data(test_query, database)
        assert correct_string == test_string

def test_table_backup_data_yes():
    """Test create_table user options"""
    with patch("builtins.input", side_effect=["New Custom Table", "3", "y"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        correct_string_1 = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query_1 = 'select * from "New Custom Table"'
        test_string_1 = schema_manager.get_data(test_query_1, database)
        correct_string_2 = """+----------+---------------+
|   Row ID | Table Title   |
+==========+===============+
|        0 | test1         |
+----------+---------------+"""
        test_query_2 = 'select * from "keys"'
        test_string_2 = schema_manager.get_data(test_query_2, backup_key)
        correct_string_3 = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query_3 = 'select * from "New Custom Table_0"'
        test_string_3 = schema_manager.get_data(test_query_3, backup_data)
        assert correct_string_1 == test_string_1
        assert correct_string_2 == test_string_2
        assert correct_string_3 == test_string_3

def test_table_backup_data_no_yes():
    """Test create_table user options"""
    with patch("builtins.input", side_effect=["New Custom Table", "3", "n", "3", "y"]):
        test_content, test_title = csv_loader.read_csv("datatables/test2.csv")
        schema_manager.create_table(test_content, test_title, database, backup_key, backup_data)
        correct_string_1 = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query_1 = 'select * from "New Custom Table"'
        test_string_1 = schema_manager.get_data(test_query_1, database)
        correct_string_2 = """+----------+---------------+
|   Row ID | Table Title      |
+==========+==================+
|        0 | test1            |
+----------+------------------+
|        1 | Custom Table     |
+----------+------------------+"""
        test_query_2 = 'select * from "keys"'
        test_string_2 = schema_manager.get_data(test_query_2, backup_key)
        correct_string_3 = """+----------+--------------+-------------+---------+
|   Row ID | First Name   | Unique ID   |      ID |
+==========+==============+=============+=========+
|        0 | Alice        | 12563U      | 1234567 |
+----------+--------------+-------------+---------+"""
        test_query_3 = 'select * from "New Custom Table_1"'
        test_string_3 = schema_manager.get_data(test_query_3, backup_data)
        assert correct_string_1 == test_string_1
        assert correct_string_2 == test_string_2
        assert correct_string_3 == test_string_3