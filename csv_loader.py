import pandas
# import sqlite3 as sql
from pathlib import Path
import schema_manager

def read_csv():
    path = input("Enter the path of the file you want to submit: ")
    #NEED TO SANITIZE THE TITLE INPUT, MAYBE EVEN THE PATH
    title = input("Enter the name of the table (no input defaults to file name):")
    if title == "":
        #Use the filename as the title
        title = Path(path).stem
    content = pandas.read_csv(path)
    return content, title

if __name__ == '__main__':
    """
    datatables/test1.csv
    Nice formatting:
    .mode box
    .headers on
    """
    file_content, table_title = read_csv()
    schema_manager.create_table(file_content, table_title)

