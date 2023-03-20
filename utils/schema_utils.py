from typing import Dict
import re
import importlib

# Define the SAS types for each SQL type
sas_data_type = {
    "INTEGER": "INT",
    "FLOAT": "FLOAT",
    "VARCHAR": "VARCHAR(255)",
    "BOOLEAN": "BOOLEAN",
    "DATE": "DATE",
    "DATETIME": "DATETIME",
    "BINARY": "BINARY",
    "COMPLEX": "COMPLEX",
}

def bq_to_sql_types(bq_dtype: str) -> str:
    sql_dtype = ''
    if bq_dtype == 'INTEGER':
        sql_dtype = 'INTEGER'
    elif bq_dtype == 'FLOAT':
        sql_dtype = 'FLOAT'
    elif bq_dtype == 'BOOLEAN':
        sql_dtype = 'BOOLEAN'
    elif bq_dtype == 'STRING':
        sql_dtype = 'VARCHAR(255)'
    elif bq_dtype == 'TIMESTAMP':
        sql_dtype = 'TIMESTAMP'
    elif bq_dtype == 'DATE':
        sql_dtype = 'DATE'
    return sql_dtype

def create_table_from_dict(table_dict: dict) -> str:
    table_ref = list(table_dict.keys())[0]
    table_name = table_ref.table_id
    columns_dict = table_dict[table_ref]
    columns_sql = []
    for col_name, col_dtype in columns_dict.items():
        col_dtype_sql = bq_to_sql_types(col_dtype)
        columns_sql.append(f'{col_name} {col_dtype_sql} NOT NULL')
    columns_sql_str = ',\n  '.join(columns_sql)
    return f'CREATE TABLE {table_name} (\n  {columns_sql_str}\n);'

def generate_sql_schema_string(schema_dict):
    """
    Takes in a dictionary representing a BigQuery schema and returns a string of SQL
    statements to create the schema.

    Parameters:
    - schema_dict (dict): a dictionary representing a BigQuery schema

    Returns:
    - sql_string (str): a string of SQL statements to create the schema
    """
    table = list(schema_dict.keys())[0]
    table_name = f"{table.dataset_id}.{table.table_id}"
    fields = schema_dict[table]
    sql_string = f"CREATE TABLE {table_name} (\n"

    for field, dtype in fields.items():
        sql_string += f"  {field} {dtype},\n"

    sql_string = sql_string.rstrip(",\n") + "\n);"
    return sql_string


# Define the function to get the SAS schema from a SQL string
def get_sas_schema(sql: str, sas_data_type: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    # Regular expression to match a CREATE TABLE statement and extract the table name and columns
    create_table_pattern = r"CREATE\s+TABLE\s+(\w+)\s*\((.+)\);"

    # Regular expression to match a column definition and extract the name and data type
    column_pattern = r"(\w+)\s+(\w+(?:\s*\(\d+\))?)\s*(?:PRIMARY KEY)?\s*(NOT NULL)?"

    # Extract the table names and column definitions from the SQL string
    matches = re.findall(create_table_pattern, sql, re.IGNORECASE | re.DOTALL)

    # Create a dictionary to hold the results
    result = {}

    # Process each CREATE TABLE statement and extract the column names and data types
    for match in matches:
        table_name = match[0]
        column_defs = match[1]

        # Extract the column names and data types from the column definitions
        columns = {}
        for column_def in column_defs.split(","):
            column_match = re.match(column_pattern, column_def.strip())
            if column_match:
                column_name = column_match.group(1)
                column_type = column_match.group(2)
                sas_type = sas_data_type.get(column_type.upper(), "VARCHAR(255)")
                columns[column_name] = sas_type

        # Add the columns to the result dictionary
        result[table_name] = columns

    if not result:
        raise ValueError("Could not find any tables in the SQL string")

    return result

# Define the function to get the final SAS schemas for all tables
def get_final_schemas(module_name: str):
    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get all variables defined in the module
    variables = vars(module)

    # Filter the variables that start with "table"
    table_vars = [var for var in variables if var.startswith("table__")]

    # Create a dictionary to hold the results
    result = {}

    # Process each variable that starts with "table"
    for table_var in table_vars:
        # Get the SQL string defining the table from the variable in the module
        sql = variables[table_var]

        # Get the table name from the SQL string
        table_name = re.search(r"CREATE\s+TABLE\s+(\w+)\s*\(", sql, re.IGNORECASE).group(1)

        # Get the SAS schema for the table
        sas_schema = get_sas_schema(sql, sas_data_type)

        # Add the SAS schema to the result dictionary
        result[table_name] = sas_schema[table_name]

    return result

def print_final_schemas(module_name: str):
    # Get the final SAS schemas for all tables
    sas_schemas = get_final_schemas(module_name)

    # Print the final SAS schemas for all tables in the desired format
    for table_name, columns in sas_schemas.items():
        print(f"Table name: {table_name}")
        print("Columns:")
        print(f"{table_name}: {columns}")
        print()

table__2 = """CREATE TABLE Location (
  city VARCHAR(255) NOT NULL,
  state VARCHAR(255) NOT NULL,
  zipcode VARCHAR(255) PRIMARY KEY
);
"""

if __name__ == "__main__":
    print(type(table__2))
    print(table__2)
    print_final_schemas("schema_utils")