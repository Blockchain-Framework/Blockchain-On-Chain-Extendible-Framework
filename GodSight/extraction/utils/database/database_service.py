import pandas as pd
from sqlalchemy import create_engine
import json
import os
from psycopg2.extras import execute_values
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, exc
from GodSight.extraction.logs.log import Logger
from GodSight.extraction.utils.database.db import connect_database

logger = Logger("GodSight")


def convert_dict_to_json(x):
    if isinstance(x, dict) or (isinstance(x, list) and all(isinstance(elem, dict) for elem in x)):
        return json.dumps(x)
    return x


def serialize_for_sql(value):
    if isinstance(value, dict):
        return json.dumps(value)  # Serialize dict to JSON string
    return value


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


def store_all_extracted_data(blockchain, subchain, date, transformed_trxs, transformed_emitted_utxos,
                             transformed_consumed_utxos, config):
    # Connect to the database
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cursor:
                # Disable autocommit for transaction
                conn.autocommit = False

                # Define a generic function to insert data
                def insert_data(transformed_data, data_type):
                    if not transformed_data:
                        return  # Skip if no data

                    # Define the table name based on the data type
                    table_mapping = {
                        'transactions': 'transaction_data',
                        'emitted_utxos': 'emitted_utxo_data',
                        'consumed_utxos': 'consumed_utxo_data'
                    }
                    table_name = table_mapping[data_type]

                    # Prepare the SQL query for inserting data
                    columns = transformed_data[0].keys()
                    sql = (f"INSERT INTO {table_name} ({', '.join(columns)}, date, blockchain, sub_chain) VALUES %s ON "
                           f"CONFLICT DO NOTHING")

                    # Prepare data tuples for insertion, including the current_date
                    values = [
                        tuple(serialize_for_sql(item) for item in row.values()) + (date, blockchain, subchain)
                        for row in transformed_data
                    ]

                    # Execute the bulk insert with execute_values for efficiency
                    execute_values(cursor, sql, values)

                # Insert data for each type
                insert_data(transformed_trxs, 'transactions')
                insert_data(transformed_emitted_utxos, 'emitted_utxos')
                insert_data(transformed_consumed_utxos, 'consumed_utxos')

                # Commit the transaction
                conn.commit()
                print("Successfully inserted all data")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Failed to store data: {e}")
        raise (e)
