import pandas as pd
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, exc

from ...config import Config

config = Config()

def execute_query(query, config):
    """
    Execute a database query safely.
    Returns a DataFrame or None if an exception occurs.
    """
    try:
        return get_query_results(query, config)
    except Exception as error:
        raise
    
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
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
        print(f"Database error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



def batch_insert_dataframes(dfs_to_insert, config):
    engine = create_engine(config.db_url)
    
    # Start a single transaction
    with engine.begin() as connection:
        for df in dfs_to_insert:
            try:
                table_name = df._table_name
                df.to_sql(table_name, connection, if_exists='append', index=False, chunksize=1000)
            except SQLAlchemyError as e:
                # Log the error and rollback the transaction
                print(f"SQLAlchemyError during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback
            except Exception as e:
                print(f"An unexpected error occurred during batch insertion into {table_name}: {e}")
                raise  # Raising an error to trigger the transaction rollback


def get_transactions(blockchain, subchain, date, config):
    query = f"SELECT * FROM {subchain}_transactions WHERE date = '{date}'"
    return get_query_results(query, config)

def get_emitted_utxos(blockchain, subchain,date, config):
    query = f"SELECT * FROM {subchain}_emitted_utxos WHERE date = '{date}'"
    return get_query_results(query, config)

def get_consumed_utxos(blockchain, subchain, date, config):
    query = f"SELECT * FROM {subchain}_consumed_utxos WHERE date = '{date}'"
    return get_query_results(query, config)

def get_blockchains(config):
    query = "SELECT DISTINCT blockchain FROM blockchain_table;"
    return get_query_results(query, config)

def get_subchains(blockchain, config):
    query =f"SELECT sub_chain FROM blockchain_table WHERE blockchain = '{blockchain}' AND sub_chain != 'default'"
    return get_query_results(query, config)

def get_subchain_metrics(blockchain, subchain, config):
    query = f"""
    SELECT m.metric_name 
    FROM metric_table m 
    JOIN chain_metric cm ON m.metric_name = cm.metric_name 
    JOIN blockchain_table b ON cm.blockchain_id = b.id 
    WHERE b.blockchain = '{blockchain}' AND b.sub_chain = '{subchain}';
    """
    return get_query_results(query, config)

def get_chain_basic_metrics(blockchain, config):
    query = f"""
    SELECT m.metric_name, m.grouping_type
    FROM metric_table m 
    JOIN chain_metric cm ON m.metric_name = cm.metric_name 
    JOIN blockchain_table b ON cm.blockchain_id = b.id 
    WHERE b.blockchain = '{blockchain}' AND m.type = 'basic';
    """
    return get_query_results(query, config)

def load_model_fields(config, table_name):
    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
    return get_query_results(query, config)

def get_general_data(blockchain, subchain, date, config):
    # Load the model fields from the database
    transaction_model_fields = load_model_fields(config, 'transaction_model')
    utxo_model_fields = load_model_fields(config, 'utxo_model')

    # Construct the SELECT statement with all the required fields
    transaction_fields = ', '.join([f"t.{field}" for field in transaction_model_fields.keys()])

    emit_utxo_fields = ', '.join([
        f"(SELECT COUNT(*) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_count",
        f"(SELECT AVG(amount) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_amount_mean",
        f"(SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_amount_median",
        f"(SELECT MIN(amount) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_amount_min",
        f"(SELECT MAX(amount) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_amount_max",
        f"(SELECT STDDEV_POP(amount) FROM {subchain}_emitted_utxos WHERE txHash = t.txHash) AS input_utxo_amount_std_dev"
    ])

    consume_utxo_fields = ', '.join([
        f"(SELECT COUNT(*) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_count",
        f"(SELECT AVG(amount) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_amount_mean",
        f"(SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_amount_median",
        f"(SELECT MIN(amount) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_amount_min",
        f"(SELECT MAX(amount) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_amount_max",
        f"(SELECT STDDEV_POP(amount) FROM {subchain}_consumed_utxos WHERE txHash = t.txHash) AS output_utxo_amount_std_dev"
    ])

    query = f"""
        SELECT {transaction_fields}, {emit_utxo_fields}, {consume_utxo_fields}
        FROM {subchain}_transactions t
        WHERE t.date = '{date}'
    """

    # Execute the query and fetch the results
    results = get_query_results(query, config)

    # Create a DataFrame from the results
    general_data = pd.DataFrame(results)

    return general_data