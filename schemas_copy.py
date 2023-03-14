from google.cloud import bigquery
from schema_utils import print_final_schemas, create_table_from_dict

table__2 = """CREATE TABLE Location (
  city VARCHAR(255) NOT NULL,
  state VARCHAR(255) NOT NULL,
  zipcode VARCHAR(255) PRIMARY KEY
);
"""

if __name__ == "__main__":
    # Get the SAS schemas for all tables
    print(type(table__2))
    print(table__2)
    print_final_schemas("schemas_copy")