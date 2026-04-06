"""
CSV Loader used to read csv files from a path and send it to the schema_manager
"""

import pandas
import logging
# import sqlite3 as sql
from pathlib import Path
import schema_manager

#ChatGPT helped
#error log file config, works globally
logging.basicConfig(
    filename="error_log.txt",          # file to write to
    level=logging.ERROR,           # only log errors and above
    #time at error - name of file error came from - severity of error - message
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def read_csv(path):
    """
    Reads a CSV located at the variable path
    Returns the CSV content and the title the user wants to have in the form of a tuple:
    (content, title) 
    """
    try:
        content = pandas.read_csv(path)
        #NEED TO SANITIZE THE TITLE INPUT, MAYBE EVEN THE PATH
        title = input("Enter the name of the table (no input defaults to file name): ")
        if title == "":
            #Use the filename as the title
            title = Path(path).stem
        return content, title
    
    except FileNotFoundError:
        logging.error("File path does not exist or is invalid.", exc_info=True)
        print("Invalid file path or file.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")

def main(path):
    """
    Runs read_csv and transfers the information to schema_manager's create table to
    to create a table
    """
    file_content, table_title = read_csv(path)
    schema_manager.create_table(file_content, table_title, 'database.db')

if __name__ == '__main__':
    main()
    # schema_manager.get_data('select "First Name", "Row Id", "School E-mail" from test1 where "Row ID" < 2')