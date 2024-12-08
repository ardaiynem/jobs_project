import sys
import os
import pandas as pd

# Add the project root directory to the Python path (since I can not use __init__.py in the infra directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from infra.postgresql_connector import PostgreSQLConnector
from infra.mongodb_connector import MongoDBConnector

def main():
    # Initialize PostgreSQL database connection
    pg_conn = PostgreSQLConnector()

    try:
        # Retrieve all processed data from 'raw_table'
        query = "SELECT * FROM raw_table;"
        result = pg_conn.execute_query(query)
        
        # Get column names from cursor description
        columns = [desc[0] for desc in pg_conn.cursor.description]
        
        # Create a DataFrame from the retrieved data
        data_df = pd.DataFrame(result, columns=columns)
        
        # Save DataFrame to CSV
        data_df.to_csv('postgres_data.csv', index=False)
        print('Data successfully exported to processed_data.csv')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        pg_conn.close_connection()

    # Initialize MongoDB database connection
    mongo_conn = MongoDBConnector()

    try:
        # Retrieve all data from 'raw_collection' collection
        result = mongo_conn.get_all_data()

        # Create a DataFrame from the retrieved data
        data_df = pd.DataFrame(result)

        # Save DataFrame to CSV
        data_df.to_csv('mongodb_data.csv', index=False)
        print('Data successfully exported to raw_data.csv')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        mongo_conn.close_connection()

if __name__ == '__main__':
    main()