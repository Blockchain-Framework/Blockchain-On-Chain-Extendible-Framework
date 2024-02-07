import pandas as pd
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, exc

def convert_dict_to_json(x):
    if isinstance(x, dict) or (isinstance(x, list) and all(isinstance(elem, dict) for elem in x)):
        return json.dumps(x)
    return x

def append_dataframe_to_sql(table_name, df, database_connection = os.environ.get("DATABASE_CONNECTION")):
    
    """
    Appends a DataFrame to a SQL table, creating the table if it doesn't exist.
    
    :param table_name: Name of the SQL table.
    :param df: DataFrame to be appended.
    :param database_connection: Database connection string.
    """
    for col in df.columns:
        df[col] = df[col].apply(convert_dict_to_json)
    
    try:
        # Create the database engine
        engine = create_engine(os.environ.get("DATABASE_CONNECTION"))

        # Create an inspector
        insp = Inspector.from_engine(engine)

        # Check if the table exists
        if insp.has_table(table_name):
            # If table exists, append data
            with engine.begin() as connection:  # Start a transaction
                df.to_sql(table_name, connection, if_exists='append', index=False, chunksize=1000)
        else:
            # If table does not exist, create it and append data
            with engine.begin() as connection:  # Start a transaction
                df.to_sql(table_name, connection, if_exists='fail', index=False, chunksize=1000)

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    
def get_query_results(query, database_connection=os.environ.get("DATABASE_CONNECTION")):
    """
    Executes a SQL query and returns the results as a DataFrame.

    :param query: SQL query to be executed.
    :param database_connection: Database connection string.
    :return: DataFrame containing the query results.
    """
    try:
        # Create the database engine
        engine = create_engine(os.environ.get("DATABASE_CONNECTION"))
        # Execute the query and fetch the results
        with engine.connect() as connection:
            results = pd.read_sql_query(query, connection)
        return results

    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
   
def batch_insert_dataframes(dfs_to_insert, database_connection=os.environ.get("DATABASE_CONNECTION")):
    print(os.environ.get("DATABASE_CONNECTION"))
    engine = create_engine("postgresql://postgres:12345@localhost:5432/onchain")
    
    # Start a single transaction
    with engine.begin() as connection:
        for df in dfs_to_insert:
            try:
                table_name = df._table_name
            
                for col in df.columns:
                    df[col] = df[col].apply(convert_dict_to_json)
            
                print(f"Inserting into table: {table_name}")  # Debug print
                assert isinstance(table_name, str), "table_name must be a string"
                df.to_sql(table_name, connection, if_exists='append', index=False, chunksize=1000)
            except SQLAlchemyError as e:
                # Log the error and rollback the transaction
                print(f"SQLAlchemyError during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback
            except Exception as e:
                print(f"An unexpected error occurred during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback

