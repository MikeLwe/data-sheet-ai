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

def read_csv():
    try:
        path = input("Enter the path of the file you want to submit: ")
        #NEED TO SANITIZE THE TITLE INPUT, MAYBE EVEN THE PATH
        title = input("Enter the name of the table (no input defaults to file name):")
        if title == "":
            #Use the filename as the title
            title = Path(path).stem
        content = pandas.read_csv(path)
        return content, title
    
    except FileNotFoundError:
        logging.error("File path does not exist or is invalid.", exc_info=True)
        print("Invalid file path or file.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("Something went wrong.")


if __name__ == '__main__':
    """
    datatables/test1.csv
    Nice formatting:
    .mode box
    .headers on
    """
    # file_content, table_title = read_csv()
    # schema_manager.create_table(file_content, table_title)
    schema_manager.get_data('select "First Name", "Row Id", "School E-mail" from test1 where "Row ID" < 2')

