from openai import OpenAI
import schema_manager

database = 'database.db'

def query_to_sql(natural_query):
    client = OpenAI()

    prompt = f"""
    You are an AI assistant tasked with converting user's natural language queries into SQL 
    statements. The database uses SQLite and contains the following tables: - sales 
    (sale_id, product_id, quantity, sale_date, revenue)  - products (product_id, product_name, 
    category, price) - employees (employee_id, name, department, hire_date) - customers 
    (customer_id, customer_name, location) User Query: {natural_query} Your task is to: 1.  
    Generate a SQL query that accurately answers the user's question and starts with SELECT. 
    2. Ensure the SQL is compatible with SQLite syntax and the database. Output Format: - SQL Query
    """
    response = client.responses.create(model="gpt-5.4",input=prompt)

    return response.output_text

if __name__ == '__main__':
    print("test")