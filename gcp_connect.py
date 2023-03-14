#%%
import os
import pandas as pd
from google.oauth2 import service_account

query = 'SELECT * FROM `bigquery-public-data.covid19_covidtracking.summary` LIMIT 100'
key_path = '/Users/kevin/Desktop/analyst-380600-f421af614bd0.json'

df = pd.read_gbq(query, 
                 project_id='analyst-380600',
                 credentials=service_account.Credentials.from_service_account_file(key_path),
                 dialect='standard',
                 )
print(df.head())

# %%
