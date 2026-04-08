"""
Tests for query_llm_test Module
"""

import query_service

database = 'test_database.db'

def test_query_llm_1():
    """Test retreiving data from test1 table"""
    correct_string = "" #data table contents
    query = ""
    test_string = query_service.run_query(query, database)
    assert correct_string == test_string