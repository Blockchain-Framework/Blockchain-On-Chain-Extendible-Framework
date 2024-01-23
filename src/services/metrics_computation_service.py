import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine
from data_storage_service import get_query_results
import sys
import logging

sys.path.insert(0, 'E:\\Uni\\Final Year Project\\Workspace\\codebase\\Blockchain-On-Chain-Extendible-Framework')

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

def trx_per_second(table, date):
    """
    Calculate transactions per second for a given table and date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for trx_per_second.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        count = results.iloc[0]['count']
        if count > 0:
            return count / 86400
        else:
            logging.info("No transactions found for the given date.")
            return 0
    return None

def trx_per_day(table, date):
    """
    Calculate transactions per day for a given table and date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for trx_per_day.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None


def avg_trx_fee():
    pass
    
    
def avg_trx_per_block(table, date):
    """
    Calculate average transactions per block for a given table and date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for avg_trx_per_block.")
        return None

    block_count_query = f"SELECT COUNT(DISTINCT \"blockHeight\") FROM {table} WHERE date = '{date}'"
    trx_count_query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    
    results_block_count = execute_query(block_count_query)
    results_trx_count = execute_query(trx_count_query)

    if results_block_count is not None and not results_block_count.empty and \
       results_trx_count is not None and not results_trx_count.empty:
        count_blocks = results_block_count.iloc[0]['count']
        count_trxs = results_trx_count.iloc[0]['count']

        if count_trxs > 0:
            return count_blocks / count_trxs
        else:
            logging.info("No transactions found for the given date.")
            return 0
    return None

def avg_trx_size():
    pass

def total_trxs():
    pass

def total_blocks():
    pass

def total_addresses():
    pass

def active_senders():
    pass

def active_addresses():
    pass

def trx_count():
    pass

def cummilative_number_of_trx():
    pass

def cummilative_number_of_contract_deployed():
    pass

def contract_calls():
    pass

def token_transfers():
    pass

def contract_creations():
    pass

def avg_trx_value():
    pass

def median_trx_value():
    pass

def avg_utxo_value():
    pass

def total_staked_amount():
    pass

def total_burned_amount():
    pass

def large_trx():
    pass

def whale_adrress_activity():
    pass

def cross_chain_whale_trx():
    pass

if __name__ == "__main__":
    trx_per_second('x_transactions', '2024-01-21')
    trx_per_day('x_transactions', '2024-01-21')
    avg_trx_per_block('x_transactions', '2024-01-21')