import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine
from .data_storage_service import get_query_results
import sys
import logging
from src.services.data_storage_service import append_dataframe_to_sql

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
            # return count / 86400
        else:
            logging.info("No transactions found for the given date.")
            add_data_to_database('trx_per_day', date, blockchain, subchain, 0)

            # return 0
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
        # return results.iloc[0]['count']
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    # return None

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
            # return count_blocks / count_trxs
        else:
            logging.info("No transactions found for the given date.")
            add_data_to_database('trx_per_day', date, blockchain, subchain, 0)
            return
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
        return
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
        return
    add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return 


def total_addresses():
    pass

def active_senders():
    pass

def active_addresses(table, date_range):
    """
    Calculate the number of unique addresses that have been active (either sending or receiving) in a given date range.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for active_addresses.")
        return None

    query = f"SELECT COUNT(DISTINCT addresses) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    
    return None


# def trx_count(table, date_range):
#     """
#     Calculate the number of transactions in a given table within a specified date range.
#     """
#     if not table or not date_range:
#         logging.error("Invalid input parameters for trx_count.")
#         return None

#     query = f"SELECT COUNT(*) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
#     results = execute_query(query)
    
#     if results is not None and not results.empty:
#         return results.iloc[0]['count']
#     return None


def cumulative_number_of_trx(table, end_date):
    """
    Calculate the cumulative number of transactions in a given table up to a specified date.
    """
    if not table or not end_date:
        logging.error("Invalid input parameters for cummilative_number_of_trx.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date <= '{end_date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None


def cummilative_number_of_contract_deployed():
    pass

def contract_calls():
    pass

def token_transfers():
    pass

def contract_creations():
    pass

def avg_trx_value(table, date_range):
    """
    Calculate the average transaction value in a given table within a specified date range.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for avg_trx_value.")
        return None

    query = f"SELECT AVG(CAST(value AS NUMERIC)) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    #print(f"Debug: SQL Query - {query}")
    results = execute_query(query)
    
    if results is not None and not results.empty:
        avg_value = results.iloc[0]['avg']
        #print(f"Debug: Results - {results}")
        #logging.info(f"Average transaction value in date range {date_range}: {avg_value}")
        return avg_value
    else:
        logging.warning(f"No data found for average transaction value in date range {date_range}.")
        return None

def median_trx_value(table, date_range):
    """
    Calculate the median transaction value in a given table within a specified date range.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for median_trx_value.")
        return None
    
    query = f"SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(value AS NUMERIC)) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    #print(f"Debug: SQL Query - {query}")
    results = execute_query(query)
    
    if results is not None and not results.empty:
        median_value = results.iloc[0]['percentile_cont']
        #print(f"Debug: Results - {results}")
        #logging.info(f"Median transaction value in date range {date_range}: {median_value}")
        return median_value
    else:
        logging.warning(f"No data found for median transaction value in date range {date_range}.")
        return None

def avg_utxo_value(table, date_range):
    """
    Calculate the average value of UTXOs in a given table within a specified date range.
    Note: This function assumes the 'value' column is of text type and casts it to a numeric type for the calculation.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for avg_utxo_value.")
        return None

    query = f"SELECT AVG(CAST(value AS NUMERIC)) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['avg']
    return None


def total_staked_amount(table, date_range):
    """
    Calculate the total amount of tokens staked in a given table within a specified date range.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for total_staked_amount.")
        return None

    query = f"SELECT SUM(amountStaked) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    return None


def total_burned_amount(table, date_range):
    """
    Calculate the total amount of tokens burned in a given table within a specified date range.
    """
    if not table or not date_range:
        logging.error("Invalid input parameters for total_burned_amount.")
        return None

    query = f"SELECT SUM(amountBurned) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    return None


def large_trx(table, date_range, threshold):
    """
    Calculate the number of large transactions exceeding a certain threshold value in a given table within a specified date range.
    Note: Assumes 'value' is stored as a text type and casts it to numeric for comparison.
    """
    if not table or not date_range or threshold is None:
        logging.error("Invalid input parameters for large_trx.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}' AND CAST(value AS NUMERIC) > {threshold}"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None


def whale_address_activity(table, date_range, threshold):
    """
    Calculate the number of transactions classified as whale activity in a given table within a specified date range.
    Whale transactions are defined as those exceeding a certain threshold value.
    Note: Assumes 'value' is stored as a text type and casts it to numeric for comparison.
    """
    if not table or not date_range or threshold is None:
        logging.error("Invalid input parameters for whale_address_activity.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}' AND CAST(value AS NUMERIC) > {threshold}"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None


def cross_chain_whale_trx(table, date_range, threshold):
    """
    Calculate the number of large cross-chain transactions in a given table within a specified date range.
    Cross-chain whale transactions are defined as those exceeding a certain threshold value and occurring across different chains.
    """
    if not table or not date_range or threshold is None:
        logging.error("Invalid input parameters for cross_chain_whale_trx.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date BETWEEN '{date_range[0]}' AND '{date_range[1]}' AND CAST(value AS NUMERIC) > {threshold} AND sourceChain != destinationChain"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None

#Realized cap
def get_avax_price_at_timestamp(timestamp):
    # This function should return the price of AVAX at the given timestamp.
    # This data might come from a historical price database or API.
    pass

def calculate_realized_cap(transactions):
    realized_cap = 0
    for tx in transactions:
        # Example for UTXOs in a transaction, adjust based on actual data structure
        for utxo in tx.get('emittedUtxos', []):
            amount_avax = int(utxo['asset']['amount'])  # Assuming amount is in the smallest unit
            timestamp = utxo['timestamp']
            price_at_time = get_avax_price_at_timestamp(timestamp)
            realized_cap += amount_avax * price_at_time

    return realized_cap

#  C chain
def count_contracts_deployed(transactions):
    contract_deployments = 0
    for tx in transactions:
        # Assuming transaction type or other indicators can specify contract deployment
        if is_contract_deployment(tx):
            contract_deployments += 1
    return contract_deployments

def count_contract_calls(transactions):
    contract_calls = 0
    for tx in transactions:
        # Assuming transaction type or other indicators can specify a contract call
        if is_contract_call(tx):
            contract_calls += 1
    return contract_calls

def count_token_transfers(transactions):
    token_transfers = 0
    for tx in transactions:
        # Check for transfer events in the transaction
        if has_token_transfer_event(tx):
            token_transfers += 1
    return token_transfers

def count_contract_creations(transactions):
    contract_creations = 0
    for tx in transactions:
        # Assuming transaction type or other indicators can specify contract creation
        if is_contract_creation(tx):
            contract_creations += 1
    return contract_creations

def is_contract_deployment(tx):
    # This is a simplification; the exact logic might depend on Avalanche's transaction structure
    return tx.get('toAddress') is None

def count_contracts_deployed(transactions):
    return sum(1 for tx in transactions if is_contract_deployment(tx))

def is_contract_call(tx):
    # Check if the transaction is to a non-null address and has non-empty input
    return tx.get('toAddress') is not None and tx.get('input') not in [None, '0x', '']

def count_contract_calls(transactions):
    return sum(1 for tx in transactions if is_contract_call(tx))

def has_token_transfer_event(tx):
    # Check for a Transfer event in the transaction logs or relevant fields
    # This is a placeholder; the actual implementation depends on how these events are represented in Avalanche transactions
    return 'Transfer' in str(tx)

def count_token_transfers(transactions):
    return sum(1 for tx in transactions if has_token_transfer_event(tx))

def is_contract_creation(tx):
    # This might involve more complex logic, possibly analyzing the transaction's input data
    # or events/logs that indicate a new contract address is being created
    return 'ContractCreation' in str(tx)  # Placeholder condition

def count_contract_creations(transactions):
    return sum(1 for tx in transactions if is_contract_creation(tx))


if __name__ == "__main__":
    # Define date ranges and thresholds for calculations
    date_single_day = '2024-01-27'
    date_range_full = ('2024-01-20', '2024-01-27')
    large_trx_threshold = 10000  # Threshold for a large transaction
    whale_trx_threshold = 50000  # Threshold for whale transactions

    # # Transactions per second
    # trx_per_sec = trx_per_second('x_transactions', date_single_day)
    # print(f"Transactions per second: {trx_per_sec}")

    # # Transactions per day
    # trx_per_day_val = trx_per_day('x_transactions', date_single_day)
    # print(f"Transactions per day: {trx_per_day_val}")

    # # Average transactions per block
    # avg_trx_block = avg_trx_per_block('x_transactions', date_single_day)
    # print(f"Average transactions per block: {avg_trx_block}")

    # # Total transactions
    # total_transactions = total_trxs('x_transactions')
    # print(f"Total transactions: {total_transactions}")

    # # Total blocks
    # total_blocks_val = total_blocks('x_transactions')
    # print(f"Total blocks: {total_blocks_val}")

    # # Number of transactions in a specific date range
    # trx_count_val = trx_count('x_transactions', date_range_full)
    # print(f"Number of transactions in date range {date_range_full}: {trx_count_val}")

    # # Cumulative number of transactions up to a specified date
    # cumulative_trx_val = cumulative_number_of_trx('x_transactions', date_single_day)
    # print(f"Cumulative number of transactions up to {date_single_day}: {cumulative_trx_val}")

    # # Average transaction value in a specific date range
    # avg_trx_value_val = avg_trx_value('x_transactions', date_range_full)
    # print(f"Average transaction value in date range {date_range_full}: {avg_trx_value_val}")

    # # Median transaction value in a specific date range
    # median_trx_value_val = median_trx_value('x_transactions', date_range_full)
    # print(f"Median transaction value in date range {date_range_full}: {median_trx_value_val}")

    # # Average UTXO Value (X-Chain)
    # avg_utxo_val_x = avg_utxo_value('x_emitted_utxos', date_range_full)
    # print(f"Average UTXO value in X-Chain date range {date_range_full}: {avg_utxo_val_x}")

    # # Large Transactions (X-Chain)
    # large_trx_val_x = large_trx('x_transactions', date_range_full, large_trx_threshold)
    # print(f"Number of large transactions in X-Chain (threshold: {large_trx_threshold}) in date range {date_range_full}: {large_trx_val_x}")

    # # Whale Address Activity (X-Chain)
    # whale_activity_val_x = whale_address_activity('x_transactions', date_range_full, whale_trx_threshold)
    # print(f"Number of whale transactions in X-Chain (threshold: {whale_trx_threshold}) in date range {date_range_full}: {whale_activity_val_x}")
    
    #Total staked amount
    staked_amount = total_staked_amount('x_emitted_utxos', date_range_full)
    print(f'Total staked amount in X-Chain (date range {date_range_full}): {staked_amount}')
