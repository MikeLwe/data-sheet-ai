"""
Tests for sql_validator Module
"""

import sql_validator
from unittest.mock import patch

database = 'test_database.db'

def test_validate_query_1():
    """Test Validate Query, default True"""
    query = 'select * from test1'
    correct_result = True
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_2():
    """Test Validate Query, default False"""
    query = 'select * from non_existent_table'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_3():
    """Test Validate Query, quotations True"""
    query = 'select * from "Custom Table"'
    correct_result = True
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_4():
    """Test Validate Query, no column detected False"""
    query = 'select * from test1 where fake_id > 0'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_5():
    """Test Validate Query, column detected True"""
    query = 'select * from test1 where "Row ID" < 2'
    correct_result = True
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_6():
    """Test Validate Query, illegal instruction (drop) False"""
    query = 'drop table test1'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_7():
    """Test Validate Query, illegal instruction (pragma) False"""
    query = 'pragma table_info("Custom Table")'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_8():
    """Test Validate Query, illegal instruction (alter) False"""
    query = 'alter table test1 drop column "First Name"'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_9():
    """Test Validate Query, illegal character (--) False"""
    query = 'drop table test1 --select * from test1'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_10():
    """Test Validate Query, illegal character (;) False"""
    query = 'select * from "Custom Table"; drop table "Custom Table"'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_11():
    """Test Validate Query, illegal instruction (truncate) False"""
    query = 'truncate table "Custom Table"'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_12():
    """Test Validate Query, illegal instruction (update) False"""
    query = 'update test1 set "Row ID" = bad'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_13():
    """Test Validate Query, illegal instruction (insert) False"""
    query = 'insert into test1 values (4, evil, person, virus@malicious.exe)'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_14():
    """Test Validate Query, illegal instruction (merge) False"""
    query = 'merge into test1 using test1'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result

def test_validate_query_15():
    """Test Validate Query, illegal instruction (create) False"""
    query = 'create table "evil table" ("evil number" INTEGER)'
    correct_result = False
    test_result = sql_validator.validate_query(query)
    assert correct_result == test_result