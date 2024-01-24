import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine
from data_storage_service import get_query_results
import sys

sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

def trx_per_second(table, date):
    query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results = get_query_results(query)
    
    # Extract the count value from the DataFrame
    count = results.iloc[0]['count']

    trx_per_second = count / 86400
    return trx_per_second

def trx_per_day(table, date):
    query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results = get_query_results(query)
    
    # Extract the count value from the DataFrame
    count = results.iloc[0]['count']

    return count


# def avg_trx_fee():
#     pass

def avg_trx_fee(table, date):
    # Estimating transaction fee based on the difference between amountUnlocked and amountCreated
    query = f"""
    SELECT AVG(amountUnlocked - amountCreated) as avg_fee
    FROM {table}
    WHERE date = '{date}' AND amountUnlocked IS NOT NULL AND amountCreated IS NOT NULL
    """
    results = get_query_results(query)
    avg_fee = results.iloc[0]['avg_fee'] if results.iloc[0]['avg_fee'] is not None else 0
    return avg_fee
    
    
def avg_trx_per_block(table, date):
    block_count_query = f"SELECT COUNT(DISTINCT \"blockHeight\") FROM {table} WHERE date = '{date}'"

    trx_count_query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results_block_count = get_query_results(block_count_query)
    results_trx_count = get_query_results(trx_count_query)

    count_blocks = results_block_count.iloc[0]['count']
    count_trxs = results_trx_count.iloc[0]['count']
    
    trx_per_block = count_blocks/count_trxs
    
    return trx_per_block

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
    # trx_per_second('x_transactions', '2024-01-21')
    # avg_trx_per_block('x_transactions', '2024-01-21')
    avg_trx_fee('x_transactions', '2024-01-21')