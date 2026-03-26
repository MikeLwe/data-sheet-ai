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

def csv_to_sql(content, title):

    # connection = sql.connect('database.db')
    # cursor = connection.cursor()


    # # run a query
    # cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} (id INTEGER, name TEXT)")

    # # insert data
    # cursor.execute("INSERT INTO users VALUES (1, 'Alice')")

    # # save changes
    # connection.commit()
    return

def type_to_sql(content):
    column_str = ""
    col_name = content.columns.tolist()
    table_types = content.dtypes
    for field in col_name:
        data_type = table_types[field]
        data_type = map_dtype_to_sql(data_type)
        column_str += f"{field} {data_type}"
    return column_str

#From ChatGPT, converting dtype result to SQL strings
def map_dtype_to_sql(dtype):
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
    file_content, table_title = read_csv()
    print(table_title)

