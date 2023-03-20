#%%
import os
import pandas as pd
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Access to personal datasets using service account
query = 'SELECT * FROM `bigquery-public-data.covid19_covidtracking.summary` LIMIT 0'
key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
project_id = os.environ.get('PROJECT_ID')

df = pd.read_gbq(query, 
                 project_id=project_id,
                 credentials=service_account.Credentials.from_service_account_file(key_path),
                 dialect='standard'
                 )
print(df.head())
print(df.dtypes)

#%%
from google.cloud import bigquery

# Access to public datasets
client = bigquery.Client(project='bigquery-public-data')
table_ref = client.dataset('covid19_covidtracking').table('summary')
table = client.get_table(table_ref)
print(table)
schema = table.schema
# print(schema)

table_dict = {table:
              {field.name: field.field_type for field in schema}}
print(table_dict)