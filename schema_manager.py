import sqlite3 as sql
import pandas
import logging

database = 'database.db'

#error log config already initialized, so unnecessary to reinitialize
logger = logging.getLogger(__name__)

def create_table(content, title):
    connection = sql.connect(database)
    cursor = connection.cursor()

    #get column headers
    col_head = col_schema(content)

    #error detection for whether to create or append table
    table_exists = table_checker(cursor, title)
    try:
        if table_exists:
            #query for user to choose to append csv contents, create new table, or stop creating table
            str_decision = input(
                "This table title already exists.\n"
                "Choose an option:\n"
                "  (1) append table content\n"
                "  (2) create new table\n"
                "  (3) stop making a table\n\n"
                "Input the choice by number: "
            )
            table_decision = int(str_decision)
            if table_decision == 1:
                print("Appending contents...")
            elif table_decision == 2:
                title = input("Creating a New Table...\nInput a new title: ")
                #DONT FORGET TO AVOID SQL INJECTION ----------------
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} ({col_head})")
            elif table_decision == 3:
                print("Stopping all actions...")
                # save changes
                connection.commit()

                #close the connection
                connection.close()
                return
            else:
                print("Invalid input. Please enter 1, 2, or 3.")

    #Log an error with a message and information such as date and time
    except ValueError:
        logging.error(f"User entered non-integer input. User input: {str_decision}", exc_info=True)
        print("Invalid input. Please enter a number.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")
        #IMPLEMENT STUFF HERE --------------------
    else:
        #DONT FORGET TO AVOID SQL INJECTION ----------------
        print("Creating table...")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} ({col_head})")

    #insert data into table
    col_name = content.columns.tolist()
    id = len(col_name)
    for i in range(id):
        values = [i] + content.iloc[i].to_list()
        #Below is ChatGPT code to help avoid SQL Injection
        #creates a list with the placeholder ? for each column
        placeholders = ', '.join(['?'] * (len(values))) 
        #DONT FORGET TO AVOID SQL INJECTION FOR TITLE ----------------
        query = f"INSERT INTO {title} VALUES ({placeholders})"
        #replaces the placeholder '?' in the query with "values"
        cursor.execute(query, values)

    # save changes
    connection.commit()

    #close the connection
    connection.close()
    print(f"Table named {title} successfully created!")
    return

def col_schema(content):
    """Format the contents of the CSV file into SQL strings"""
    #CONSIDER SQL INJECTION WITH COLUMN HEADERS AND ERRORS ASSOCIATED WITH THEM
    #EMPTY HEADER?
    column_str = ""
    column_elements = []
    column_elements.append('"Row ID" INTEGER')
    col_name = content.columns.tolist()
    table_types = content.dtypes
    for field in col_name:
        data_type = table_types[field]
        data_type = map_dtype_to_sql(data_type)
        column_elements.append(f'"{field}" {data_type}')
    column_str = ", ".join(column_elements)
    return column_str

def table_checker(cursor, title):
    """Checks if a table exists in the database or not"""
    #help from stackoverflow (1)
    cursor.execute(f"SELECT  name FROM sqlite_master WHERE type='table' AND name=?",(title,))
    count = cursor.fetchone()
    if count:
        return True
    else:
        return False

#From ChatGPT
def map_dtype_to_sql(dtype):
    """
    Converting dtype result to SQL type strings
    Parameter: dtype (string) - the data type of a column in a csv
    """
    if pandas.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pandas.api.types.is_float_dtype(dtype):
        return "REAL"
    elif pandas.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pandas.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "TEXT"
    
if __name__ == '__main__':
    print("test")
