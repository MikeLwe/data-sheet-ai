import sql_validator
import llm
import schema_manager
import logging

logger = logging.getLogger(__name__)
database = 'database.db'

def main(natural_query):
    """
    Runs the LLM with the natural_query as the input and validates the LLM's query.
    Prints the contents of the table with schema_manager's get_data function 
    """
    #llm converts this query to sql
    query = llm.query_to_sql(natural_query)
    try:
        test_query = sql_validator.validate_query(query)
        if test_query:
            table_content = schema_manager.get_data(query, database)
            print(table_content)
        else:
            print("Validator Rejected Query")

    except Exception as e:
        logging.error(f"Unsure of the error." 
                      "User Input: {natural_query}, SQL Conversion: {query}",
                      exc_info=True)
        print("An Unexpected Error Occurred.")

if __name__ == '__main__':
    query = input("What would you like to get?\n")
    main(query)