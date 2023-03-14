from google.cloud import bigquery
from schema_utils import print_final_schemas, create_table_from_dict

# WARNING: keyword "table__" is reserved in inside schema_utils.py

# Test with an example SQL string defining two tables
# table__1 = """
# CREATE TABLE Person (
#   id INTEGER PRIMARY KEY,
#   age INTEGER NOT NULL,
#   gender VARCHAR(255) NOT NULL,
#   city VARCHAR(255) NOT NULL,
#   state VARCHAR(255) NOT NULL,
#   height INTEGER NOT NULL,
#   weight FLOAT NOT NULL
# );
# """
# table__2 = """CREATE TABLE Location (
#   city VARCHAR(255) NOT NULL,
#   state VARCHAR(255) NOT NULL,
#   zipcode VARCHAR(255) PRIMARY KEY
# );
# """

# Access to public datasets
client = bigquery.Client(project='bigquery-public-data')
tableref = client.dataset('covid19_covidtracking').table('summary')
table = client.get_table(tableref)
schema = table.schema

# form schema dictionary to pass to generate_sql_schema_string
schema_dict = {table:
              {field.name: field.field_type for field in schema}
              }

table__3 = create_table_from_dict(schema_dict)


if __name__ == "__main__":
    # Get the SAS schemas for all tables
    # print(type(table__2))
    # print(table__2)
    # print(table__3)
    print_final_schemas("schemas")