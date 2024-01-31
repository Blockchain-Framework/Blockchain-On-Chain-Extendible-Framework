import pandas as pd
import psycopg2
import sys
import logging
import os
# sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from utils.database_service import get_query_results, append_dataframe_to_sql

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def execute_query(query):
    """
    Execute a database query safely.
    Returns a DataFrame or None if an exception occurs.
    """
    try:
        return get_query_results(query)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Database error: {error}")
        return None

def key_mapper(key):
    def decorator(func):
        func._key = key
        return func
    return decorator


def add_data_to_database(table, date, blockchain, subChain, value):
    result_df = pd.DataFrame({
        'date': [date],
        'blockchain': [blockchain],
        'subchain':[subChain],
        'value': [value]
    })

    # Insert result into database
    append_dataframe_to_sql('metrics_table', result_df)
    
  
@key_mapper("trx_per_second")
def trx_per_second(blockchain, subchain, date):
    """
    Calculate transactions per second for a given table and date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for trx_per_second.")
        return None

    query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        count = results.iloc[0]['count']
        if count > 0:
            add_data_to_database('trx_per_day', date, blockchain, subchain, count / 86400)
            return count / 86400
        else:
            logging.info("No transactions found for the given date.")
            add_data_to_database('trx_per_day', date, blockchain, subchain, 0)

            return 0
    return None

@key_mapper("trx_per_day")
def trx_per_day(blockchain, subchain, date):
    """
    Calculate transactions per day for a given table and date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for trx_per_day.")
        return None

    query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        add_data_to_database('trx_per_day', date, blockchain, subchain, results.iloc[0]['count'])
        return results.iloc[0]['count']
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return None

def avg_trx_fee():
    pass

@key_mapper("avg_trx_per_block")
def avg_trx_per_block(blockchain, subchain, date):
    """
    Calculate average transactions per block for a given table and date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_trx_per_block.")
        return None

    block_count_query = f"SELECT COUNT(DISTINCT \"blockHeight\") FROM {subchain}_transactions WHERE date = '{date}'"
    trx_count_query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
    
    results_block_count = execute_query(block_count_query)
    results_trx_count = execute_query(trx_count_query)

    if results_block_count is not None and not results_block_count.empty and \
       results_trx_count is not None and not results_trx_count.empty:
        count_blocks = results_block_count.iloc[0]['count']
        count_trxs = results_trx_count.iloc[0]['count']

        if count_trxs > 0:
            add_data_to_database('trx_per_day', date, blockchain, subchain, count_blocks / count_trxs)
            return count_blocks / count_trxs
        else:
            logging.info("No transactions found for the given date.")
            add_data_to_database('trx_per_day', date, blockchain, subchain, 0)
            return 0
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return None

def avg_trx_size():
    pass

@key_mapper("total_trxs")
def total_trxs(blockchain, subchain, date):
    """
    Calculate the total number of transactions in a given table.
    """
    if not subchain:
        logging.error("Invalid input parameter for total_trxs.")
        return None

    query = f"SELECT COUNT(*) FROM {subchain}_transactions"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        add_data_to_database('trx_per_day', date, blockchain, subchain, results.iloc[0]['count'])
        return results.iloc[0]['count']
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return

@key_mapper("total_blocks")
def total_blocks(blockchain, subchain, date):
    """
    Calculate the total number of blocks in a given table.
    """
    if not subchain:
        logging.error("Invalid input parameter for total_blocks.")
        return None

    query = f"SELECT COUNT(DISTINCT \"blockHash\") FROM {subchain}_transactions"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        add_data_to_database('trx_per_day', date, blockchain, subchain,  results.iloc[0]['count'])
        return results.iloc[0]['count']
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return None

