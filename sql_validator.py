"""
SQL Validator ensures that a query is:
1. check if a query is valid for the database
2. ensure that the query is not illegal
"""

import sqlite3 as sql
import logging
import sqlparse
from sqlparse.tokens import Keyword, Comment, Punctuation

logger = logging.getLogger(__name__)
database = 'database.db'

def validate_query(query):
    """
    Validates whether a query is allowed to be run
    """
    try:
        connection = sql.connect(database)
        cursor = connection.cursor()

        query = sqlparse.split(query)[0]

        #chatgpt suggestion:
        # EXPLAIN checks syntax without running the query
        cursor.execute("EXPLAIN " + query)

        query_test = string_check(query)
        return query_test

    except sql.OperationalError as e:
        logging.error(f"Invalid query: {query}, {e}", exc_info=True)
        print("SQL Query is invalid for the database.")
        return False
    
    except ValueError as e:
        logging.error(f"Illegal query detected: {query}, {e}", exc_info=True)
        print("SQL Query has prohibited characters.")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

#chatgpt helped a lot with this
def string_check(query):
    """
    Checks a query for illegal commands and returns an error if it is
    """
    prohibited_keywords = {"DROP", "DELETE", "TRUNCATE", "ALTER", "SET", "INSERT", "UPDATE", "UNION", "MERGE", "CREATE"}
    query = query.upper()
    parsed = sqlparse.parse(query)

    for stmt in parsed:
        # Only allow SELECT statements
        if stmt.get_type() != "SELECT":
            raise ValueError("Only SELECT statements allowed")

        for token in stmt.tokens:
            # Disallow comments
            if token.ttype in Comment:
                raise ValueError(f"Comment detected: {token.value}")
            # Disallow semicolons
            if token.ttype in Punctuation and token.value == ";":
                raise ValueError("Semicolons are not allowed")
            # Disallow dangerous keywords
            if token.ttype is Keyword and token.value.upper() in prohibited_keywords:
                raise ValueError(f"Disallowed keyword detected: {token.value}")

    return True