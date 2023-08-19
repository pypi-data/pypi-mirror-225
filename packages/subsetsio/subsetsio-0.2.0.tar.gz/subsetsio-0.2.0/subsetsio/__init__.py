import requests
import pandas as pd

class SubsetsError(Exception):
    pass

BASE_URL = 'https://api.subsets.io'

def query(sql, api_key):
    if not sql or sql.strip() == '':
        raise SubsetsError("Query cannot be empty.")
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key  # Use x-api-key header instead of Authorization
    }
    print(f'{BASE_URL}/engine/api')

    response = requests.post(f'{BASE_URL}/engine/sql', 
                             headers=headers,
                             json={'sqlQuery': sql})

    if response.status_code != 200:
        raise SubsetsError(response.text)
    
    data = response.json()
    # Extract column names
    column_names = [col['name'] for col in data['columns']]

    # Convert the result into a pandas dataframe
    df = pd.DataFrame(data=data['data'], columns=column_names)
    return df
