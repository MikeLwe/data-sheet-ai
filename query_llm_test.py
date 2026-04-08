"""
Tests for query_llm_test Module
"""

import query_service
from unittest.mock import patch

database = 'test_database.db'

def test_query_llm_1():
    """Test retreiving data from test1 table"""
    correct_string = """+--------------+-------------+
| First Name   | Last Name   |
+==============+=============+
| Bryce        | B           |
+--------------+-------------+
| Carlos       | C           |
+--------------+-------------+""" #data table contents
    query = "give me the full names of students from test1 with a row id greater than 0"
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string

def test_query_llm_2():
    """Test retreiving data from test1 table"""
    correct_string = """+-----------------+
| School E-mail   |
+=================+
| alice@bu.edu    |
+-----------------+
| bryce@bu.edu    |
+-----------------+""" #data table contents
    query = "show the emails of students with row id less than 2"
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string

def test_query_llm_3():
    """Test unusual query on customers table"""
    correct_string = """No elements found matching that exact query. Please try again.""" #data table contents
    query = "return the customers names that are from the USA"
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string

def test_query_llm_4():
    """Test usual query on customers table"""
    correct_string = """+--------------+-------------+--------------------------+                         
| First Name   | Last Name   | Country                  |
+==============+=============+==========================+
| Rickey       | Mays        | United States of America |
+--------------+-------------+--------------------------+
| Kurt         | Prince      | United States of America |
+--------------+-------------+--------------------------+
| Johnny       | Randolph    | United States of America |
+--------------+-------------+--------------------------+
| Bryan        | Sampson     | United States of America |
+--------------+-------------+--------------------------+
| Molly        | Prince      | United States of America |
+--------------+-------------+--------------------------+""" #data table contents
    query = "show me the names and countries of customers from the United States of America"
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string

def test_query_llm_5():
    """Test retreiving data from test1 table"""
    correct_string = """+--------------+-------------+---------------+
| First Name   | Last Name   | Country       |
+==============+=============+===============+
| Ryan         | Li          | Liechtenstein |
+--------------+-------------+---------------+
| Darrell      | Santos      | Liechtenstein |
+--------------+-------------+---------------+
| Cassidy      | Dillon      | Liechtenstein |
+--------------+-------------+---------------+
| Priscilla    | Stuart      | Liechtenstein |
+--------------+-------------+---------------+
| Leslie       | Howe        | Liechtenstein |
+--------------+-------------+---------------+
| Max          | Rasmussen   | Liechtenstein |
+--------------+-------------+---------------+
| Rita         | Hutchinson  | Liechtenstein |
+--------------+-------------+---------------+
| Mindy        | Christian   | Liechtenstein |
+--------------+-------------+---------------+
| Sheryl       | Delgado     | Liechtenstein |
+--------------+-------------+---------------+
| Colin        | Doyle       | Liechtenstein |
+--------------+-------------+---------------+
| Dominique    | Benjamin    | Liechtenstein |
+--------------+-------------+---------------+
| Bill         | Richards    | Liechtenstein |
+--------------+-------------+---------------+""" #data table contents
    query = "please show me the names of customer from the most common country and the country in the data"
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string