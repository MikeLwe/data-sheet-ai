#Ensure results are valid
# -table exists, columns are right

#Words to avoid Drop, Inject, Set/Corruption?
#Protect database from LLM query

#Make sure errors/catches are notified in error_log and printed
#back to the user

import sqlite3 as sql

#temporary code for understanding
def validate_query(query, database):
    try:
        connection = sql.connect(database)
        cursor = connection.cursor()

        # EXPLAIN checks syntax without running the query
        cursor.execute("EXPLAIN " + query)

        

        return True, "Query is valid"

    except sql.OperationalError as e:
        return False, f"Invalid query: {e}"

    finally:
        cursor.close()
        connection.close()