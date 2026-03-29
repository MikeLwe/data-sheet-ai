import sqlite3 as sql
import pandas

database = 'database.db'

def create_table(content, title):
    connection = sql.connect(database)
    cursor = connection.cursor()

    #create a table
    col_head = col_schema(content)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {title} ({col_head})")

    #insert data into table
    col_name = content.columns.tolist()
    id = len(col_name)
    for i in range(id):
        values = content.iloc[i].to_list()
        value_string = ', '.join(values)
        cursor.execute(f"INSERT INTO {title} VALUES {value_string})")

    # save changes
    connection.commit()

    #close the connection
    connection.close()
    return


def col_schema(content):
    column_str = ""
    column_elements = []
    col_name = content.columns.tolist()
    table_types = content.dtypes
    for field in col_name:
        data_type = table_types[field]
        data_type = map_dtype_to_sql(data_type)
        column_elements.append(f'"{field}" {data_type}')
    column_str = ", ".join(column_elements)
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
    print("test")

    # correct_data = pandas.DataFrame({
    #     "First Name": ["Alice", "Bryce", "Carlos"],
    #     "Last Name": ["A", "B", "C"],
    #     "School E-mail": ["alice@bu.edu", "bryce@bu.edu", "carl@bu.edu"]
    # })
    # test = correct_data.iloc[0].to_list()
    # print(test)
