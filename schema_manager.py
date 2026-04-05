import sqlite3 as sql
import pandas
import logging
import numpy as np
from tabulate import tabulate

database = 'database.db'

#error log config already initialized, so unnecessary to reinitialize
logger = logging.getLogger(__name__)

def confirm(prompt="Are you sure you want to proceed? (y/n): "):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes", "Y", "Yes"):
            return True
        elif choice in ("n", "no", "N", "No"):
            return False
        else:
            print("Please enter 'y' or 'n'.")
            raise ValueError("Invalid User Input for Confirm Prompt.")

def create_table(content, title):
    connection = sql.connect(database)
    cursor = connection.cursor()

    #get column headers
    col_head = col_schema(content)

    #error detection for whether to create or append table
    table_exists = table_checker(cursor, title)
    try:
        if table_exists:
            #query for user to choose to append csv contents, create new table, 
            #overwrite the data and create a new table or stop creating table
            str_decision = input(
                "This table title already exists.\n"
                "Choose an option:\n"
                "  (1) append table content\n"
                "  (2) create new table\n"
                "  (3) replace the existing table\n"
                "  (4) stop making a table\n\n"
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
                #SOFT DELETE, make copy of table in deleted tables folder
                print("Replacing a table CANNOT be undone.")
                misinput_safety = confirm()
                if misinput_safety:
                    print("Deleting old table...")
                    cursor.execute(f"DROP TABLE {title}")
                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} ({col_head})")
                else:
                    #IMPLEMENT-------
                    print("supposed to repeat user query")

            elif table_decision == 4:
                print("Stopping all actions...")
                # save changes
                connection.commit()

                #close the connection
                connection.close()
                return
            else:
                print("Invalid input. Please enter 1, 2, 3, or 4.")

    #Log an error with a message and information such as date and time
    except ValueError:
        logging.error(f"User entered an invalid input. User input: {str_decision}", exc_info=True)
        print("Invalid input.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")
    else:
        #DONT FORGET TO AVOID SQL INJECTION ----------------
        print("Creating table...")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} ({col_head})")

    #insert data into table
    #CHANGE BELOW LINE LATER FOR EMPTY TABLE WITH COLUMNS
    first_col_values = content.iloc[:,0].tolist()
    num_rows = len(first_col_values)
    for i in range(num_rows):
        values = [i] + content.iloc[i].tolist()
        #Below is ChatGPT code to help avoid SQL Injection
        #creates a list with the placeholder ? for each column
        values = [
            int(v) if isinstance(v, (np.integer, np.int64, np.int32)) else
            float(v) if isinstance(v, (np.floating, np.float64, np.float32)) else
            v
            for v in values
        ]
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
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",(title,))
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
    elif pandas.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "TEXT"

def get_data(query):
    connection = sql.connect(database)
    # connection.row_factory = sql.Row
    cursor = connection.cursor()

    cursor.execute(query)

    #ChatGPT help for formatting
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    print(tabulate(rows, headers=columns, tablefmt="grid"))


    cursor.close()
    connection.close()

    return
    
if __name__ == '__main__':
    print("test")