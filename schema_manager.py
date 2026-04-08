"""
Schema Manager handles everything related to the database.
It creates tables to be put in the database, provides users title options for table creation,
and returns information about tables in the database.
"""

import sqlite3 as sql
import pandas
import logging
import numpy as np
import re
from tabulate import tabulate

database = 'database.db'
backup_key = 'backup_keys.db'
backup_data = 'backup.db'

#error log config already initialized, so unnecessary to reinitialize
logger = logging.getLogger(__name__)

def create_table(content, title, database, backup_key, backup_data):
    """
    Creates a table based on the content and title in the selected database
    """
    connection = sql.connect(database)
    cursor = connection.cursor()

    #get column headers
    col_head = col_schema(content)

    #error detection for whether to create or append table
    title = sanitize_text(title)
    table_exists = table_checker(cursor, title)

    #variable to remember table length to add later
    existing_row_count = 0
    try:
        if table_exists:
            while True:
                #query for user to choose to append csv contents, create new table, 
                #overwrite the data and create a new table or stop creating table
                str_decision = input(
                    "This table title already exists.\n"
                    "Choose an option:\n"
                    "  (1) append ALL row contents\n"
                    "  (2) create new table\n"
                    "  (3) replace the existing table\n"
                    "  (4) stop making a table\n\n"
                    "Input the choice by number: "
                )
                table_decision = int(str_decision)
                if table_decision == 1:
                    #APPEND ROWS, append rows with matching columns, otherwise error
                    print("Appending row contents...")
                    cursor.execute(f'SELECT COUNT(*) FROM "{title}"')
                    existing_row_count = cursor.fetchone()[0]
                    break
                elif table_decision == 2:
                    #NEW NAME, make a table with a different name
                    print("Creating a New Table...")
                    #loop to give user option for multiple titles in case invalid
                    while True:
                        new_title = input("Input a new title: ")
                        title = sanitize_text(new_title)
                        if title != "" and not table_checker(cursor, title):
                            cursor.execute(f'CREATE TABLE IF NOT EXISTS "{title}" ({col_head})')
                            break
                        else:
                            print("Invalid Title. Please try again.")
                    break
                elif table_decision == 3:
                    #SOFT DELETE, make copy of table in deleted tables folder
                    print("Replacing a table CANNOT be undone.")
                    misinput_safety = confirm()
                    if misinput_safety:
                        backup_title = make_backup(cursor, title, backup_key, backup_data)
                        print("Deleting old table...")
                        cursor.execute(f'DROP TABLE "{backup_title}"')
                        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{title}" ({col_head})')
                        break

                elif table_decision == 4:
                    #STOP, closes everything and ends action
                    print("Stopping all actions...")
                    #saves changes
                    connection.commit()

                    #closes the connection
                    connection.close()
                    return
                else:
                    print("Invalid input. Please enter 1, 2, 3, or 4.")

        else:
            #This path is for creating a table if there is no conflict
            print("Creating table...")
            cursor.execute(f'CREATE TABLE IF NOT EXISTS "{title}" ({col_head})')

    #Log an error with a message and information such as date and time
    except ValueError:
        logging.error(f"User entered an invalid input. User input: {str_decision}", exc_info=True)
        print("Invalid input.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")

    #insert data into table
    #CHANGE BELOW LINE LATER FOR EMPTY TABLE WITH COLUMNS
    num_rows = len(content)
    all_rows = []
    for i in range(num_rows):
        values = [i+existing_row_count] + content.iloc[i].tolist()
        #Below is ChatGPT code to help avoid SQL Injection
        #creates a list with the placeholder ? for each column
        values = [
            int(v) if isinstance(v, (np.integer, np.int64, np.int32)) else
            float(v) if isinstance(v, (np.floating, np.float64, np.float32)) else
            v
            for v in values
        ]
        placeholders = ', '.join(['?'] * (len(values)))
        all_rows.append(values)
        #replaces the placeholder '?' in the query with "values"
        
    cursor.executemany(f'INSERT INTO "{title}" VALUES ({placeholders})', all_rows)

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
    try:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",(title,))
        count = cursor.fetchone()
        if count:
            return True
        else:
            return False
    except sql.OperationalError:
        logging.error(f"Title is incorrect here {title}", exc_info=True)
        print("Something went wrong...")
    except Exception:
        logging.error("Something went wrong.", exc_info=True)
        print("Unexpected Error.")

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
    
def confirm(prompt="Are you sure you want to proceed? (y/n): "):
    """Generic confirmation function to see if the user wants to proceed"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes", "Y", "Yes"):
            return True
        elif choice in ("n", "no", "N", "No"):
            return False
        else:
            print("Please enter 'y' or 'n'.")

def sanitize_text(text):
    """Sanitizes text to remove potentially harmful characters"""
    #ChatGPT helped with the re import and usage
    #remove invalid characters
    text = re.sub(r"[^A-Za-z0-9_ ]+", "", text)
    return text

def make_backup(cursor, title, backup_key, backup_data):
    """Creates a backup of a table named title in the database that the cursor is pointing to"""
    #connect to the backup_key while having cursor connected to the database
    connection = sql.connect(backup_key)
    key = connection.cursor()

    #create keys table if it doesn't exist and make a list of backup tables
    key.execute(f'CREATE TABLE IF NOT EXISTS keys ("Row ID" INTEGER, "Table Title" TEXT)')

    key.execute("SELECT COUNT(*) FROM keys")
    key_count = key.fetchone()[0]

    key.execute("INSERT INTO keys VALUES (?, ?)", (key_count, title))

    #connect backup tables database with true database and copy the specified table over
    cursor.execute(f'ATTACH DATABASE "{backup_data}" AS backup_data')

    title = sanitize_text(title)

    new_title = f"{title}_{key_count}"
    cursor.execute(f'ALTER TABLE "{title}" RENAME to "{new_title}"')

    query = f'CREATE TABLE backup_data."{new_title}" AS SELECT * FROM "{new_title}"'
    cursor.execute(query)

    connection.commit()
    key.close()
    connection.close()

    #return the new title so that outside function will know what the new name is
    return new_title

def get_schema(database):
    """Retrieves the schema information of all tables of a database for the LLM prompt"""
    prompt_tables = ""
    connection = sql.connect(database)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

        tables = cursor.fetchall()

        #ChatGPT help for formatting
        table_names = [table[0] for table in tables]

        for title in table_names:
            cursor.execute(f'PRAGMA table_info("{title}")')
            columns = cursor.fetchall()
            column_names = [f'"{col[1]}"' for col in columns]
            column_names = ", ".join(column_names)
            prompt_tables = f'{prompt_tables} - "{title}" ({column_names})'

    except sql.OperationalError:
        logging.error(f"The query is invalid.", exc_info=True)
        print("The query was somehow invalid.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")

    finally:
        cursor.close()
        connection.close()
        return prompt_tables


def get_data(query, database):
    """Returns the contents of a table in database based on the SQL query"""
    connection = sql.connect(database)
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        #ChatGPT help for formatting
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

    except sql.OperationalError:
        logging.error(f"The query is invalid. Query: {query}", exc_info=True)
        print("The query was somehow invalid.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")

    finally:
        cursor.close()
        connection.close()
        return tabulate(rows, headers=columns, tablefmt="grid")