import pandas as pd
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, exc
from logs.log import Logger

logger = Logger("GodSight")

def convert_dict_to_json(x):
    if isinstance(x, dict) or (isinstance(x, list) and all(isinstance(elem, dict) for elem in x)):
        return json.dumps(x)
    return x

def append_dataframe_to_sql(table_name, df, config):
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
        engine = create_engine(config.db_url)

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
        logger.log_error(f"Error: {e}")
        
    except Exception as e:
        logger.log_error(f"An unexpected error occurred: {e}")
        
    
def get_query_results(query, config):
    """
    Executes a SQL query and returns the results as a DataFrame.

    :param query: SQL query to be executed.
    :param database_connection: Database connection string.
    :return: DataFrame containing the query results.
    """
    try:
        # Create the database engine
        engine = create_engine(config.db_url)
        # Execute the query and fetch the results
        with engine.connect() as connection:
            results = pd.read_sql_query(query, connection)
        return results

    except exc.SQLAlchemyError as e:
        logger.log_error(f"Database error: {e}")

    except Exception as e:
        logger.log_error(f"An unexpected error occurred: {e}")
   
def batch_insert_dataframes(dfs_to_insert, config):
    engine = create_engine(config.db_url)
    
    # Start a single transaction
    with engine.begin() as connection:
        for df in dfs_to_insert:
            try:
                table_name = df._table_name
                for col in df.columns:
                    df[col] = df[col].apply(convert_dict_to_json)
                logger.log_info(f"Inserting into table: {table_name}")
                assert isinstance(table_name, str), "table_name must be a string"
                df.to_sql(table_name, connection, if_exists='append', index=False, chunksize=1000)
            except SQLAlchemyError as e:
                # Log the error and rollback the transaction
                logger.log_error(f"SQLAlchemyError during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback
            except Exception as e:
                logger.log_error(f"An unexpected error occurred during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback

