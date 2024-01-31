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

def total_trxs(table, date):
    """
    Calculate the total number of transactions in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for total_trxs.")
        return None

    query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None

def avg_trx_amount(consumed_table, date):
    """
    Calculate the average transaction amount in a given consumed table for a specified date.
    """
    if not consumed_table or not date:
        logging.error("Invalid input parameters for avg_trx_amount.")
        return None

    # Query for the sum of transaction amounts and count of transactions
    query = f"""
    SELECT SUM(CAST(amount AS NUMERIC)) as total_amount, COUNT(*) as trx_count
    FROM {consumed_table}
    WHERE date = '{date}'
    """
    results = execute_query(query)

    if results is not None and not results.empty:
        total_amount = results.iloc[0]['total_amount']
        trx_count = results.iloc[0]['trx_count']

        if trx_count > 0:
            return total_amount / trx_count
        else:
            logging.info("No transactions found for the given date.")
            return 0
    return None

def avg_trxs_per_hour(table, date):
    """
    Calculate the average number of transactions per hour for a given table and date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for avg_trxs_per_hour.")
        return None

    # Query for total number of transactions
    trx_count_query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}'"
    trx_results = execute_query(trx_count_query)

    if trx_results is not None and not trx_results.empty:
        count_trxs = trx_results.iloc[0]['count']
        hours_in_day = 24
        return count_trxs / hours_in_day
    else:
        logging.info("No transactions found for the given date.")
        return 0

def total_blocks(table, date):
    """
    Calculate the total number of blocks in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for total_blocks.")
        return None

    query = f"SELECT COUNT(DISTINCT \"blockHash\") FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None

def average_tx_per_block(table, date):
    """
    Calculate the average number of transactions per block in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for average_tx_in_a_block.")
        return None

    query = f"""
    SELECT AVG(tx_count) as average_tx_per_block
    FROM (
        SELECT \"blockHash\", COUNT(*) as tx_count
        FROM {table}
        WHERE date = '{date}'
        GROUP BY \"blockHash\"
    ) as block_transactions
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['average_tx_per_block']
    return None

def active_addresses(emitted_table, consumed_table, date):
    """
    Calculate the number of unique addresses that have been active (either sending or receiving) on a given date.
    """
    if not emitted_table or not consumed_table or not date:
        logging.error("Invalid input parameters for active_addresses.")
        return None

    query = f"""
    SELECT COUNT(DISTINCT addresses) FROM (
        SELECT addresses FROM {emitted_table} WHERE date = '{date}'
        UNION
        SELECT addresses FROM {consumed_table} WHERE date = '{date}'
    ) AS active_addresses
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['count']
    return None

def active_senders(consumed_table, date):
    """
    Calculate the number of unique active senders (addresses) on a given date using the consumed table.
    Active senders are defined as addresses that have sent (consumed) on the specified date.
    """
    if not consumed_table or not date:
        logging.error("Invalid input parameters for active_senders.")
        return None

    query = f"""
    SELECT COUNT(DISTINCT addresses) as active_senders_count
    FROM {consumed_table}
    WHERE date = '{date}'
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['active_senders_count']
    return None

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

def sum_emitted_utxo_amount(table, date):
    """
    Calculate the sum of emitted UTXO amounts in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for sum_emitted_utxo_amount.")
        return None

    query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    else:
        logging.warning(f"No data found for sum of emitted UTXO amounts on {date}.")
        return None 

def avg_emmited_utxo_amount(table, date):
    """
    Calculate the average transaction value in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for avg_trx_value.")
        return None

    query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['avg']
    else:
        logging.warning(f"No data found for average transaction value on {date}.")
        return None

def median_emmited_utxo_amount(table, date):
    """
    Calculate the median transaction value in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for median_trx_value.")
        return None
    
    query = f"SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['percentile_cont']
    else:
        logging.warning(f"No data found for median transaction value on {date}.")
        return None

def sum_consumed_utxo_amount(table, date):
    """
    Calculate the sum of consumed UTXO amounts in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for sum_consumed_utxo_amount.")
        return None

    query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    else:
        logging.warning(f"No data found for sum of consumed UTXO amounts on {date}.")
        return None

def avg_consumed_utxo_amount(table, date):
    """
    Calculate the average consumed UTXO value in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for avg_consumed_utxo_amount.")
        return None

    query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['avg']
    else:
        logging.warning(f"No data found for average consumed UTXO value on {date}.")
        return None

def median_consumed_utxo_amount(table, date):
    """
    Calculate the median consumed UTXO value in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for median_consumed_utxo_amount.")
        return None
    
    query = f"SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['percentile_cont']
    else:
        logging.warning(f"No data found for median consumed UTXO value on {date}.")
        return None

def total_staked_amount(table, date):
    """
    Calculate the total amount of tokens staked in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for total_staked_amount.")
        return None

    query = f"SELECT SUM(CAST(\"amountStaked\" AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    return None

def total_burned_amount(table, date):
    """
    Calculate the total amount of tokens burned in a given table for a specified date.
    """
    if not table or not date:
        logging.error("Invalid input parameters for total_burned_amount.")
        return None

    query = f"SELECT SUM(CAST(\"amountBurned\" AS NUMERIC)) FROM {table} WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['sum']
    return None

def large_trx(emitted_table, consumed_table, date, threshold):
    """
    Calculate the number of large transactions where either the emitted or consumed amount exceeds a certain threshold value
    for specified emitted and consumed tables on a given date.
    """
    if not emitted_table or not consumed_table or not date or threshold is None:
        logging.error("Invalid input parameters for large_trx.")
        return None

    query = f"""
    WITH emitted AS (
        SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_emitted
        FROM {emitted_table}
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    ),
    consumed AS (
        SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_consumed
        FROM {consumed_table}
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    )
    SELECT COUNT(DISTINCT \"txHash\") as large_transactions_count
    FROM (
        SELECT \"txHash\" FROM emitted
        UNION
        SELECT \"txHash\" FROM consumed
    ) as combined
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['large_transactions_count']
    return None

def whale_address_activity(emitted_table, consumed_table, date, threshold):
    """
    Calculate the number of whale transactions where either the emitted or consumed amount exceeds a certain threshold value
    for specified emitted and consumed tables on a given date.
    """
    if not emitted_table or not consumed_table or not date or threshold is None:
        logging.error("Invalid input parameters for whale_address_activity.")
        return None

    query = f"""
    WITH whale_emitted AS (
        SELECT \"txHash\"
        FROM {emitted_table}
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    ),
    whale_consumed AS (
        SELECT \"txHash\"
        FROM {consumed_table}
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    )
    SELECT COUNT(DISTINCT \"txHash\") as whale_transactions_count
    FROM (
        SELECT \"txHash\" FROM whale_emitted
        UNION
        SELECT \"txHash\" FROM whale_consumed
    ) as combined_whale_transactions
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        return results.iloc[0]['whale_transactions_count']
    return None

# def cross_chain_whale_trx(table, date, threshold):
#     """
#     Calculate the number of large cross-chain transactions in a given table for a specified date.
#     Cross-chain whale transactions are defined as those exceeding a certain threshold value and occurring across different chains.
#     """
#     if not table or not date or threshold is None:
#         logging.error("Invalid input parameters for cross_chain_whale_trx.")
#         return None

#     query = f"SELECT COUNT(*) FROM {table} WHERE date = '{date}' AND CAST(value AS NUMERIC) > {threshold} AND sourceChain != destinationChain"
#     results = execute_query(query)
    
#     if results is not None and not results.empty:
#         return results.iloc[0]['count']
#     return None

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
    date_single_day = '2024-01-20'
    date_range_full = ('2024-01-20', '2024-01-27')
    large_trx_threshold = 10000  # Threshold for a large transaction
    whale_trx_threshold = 8000000000000  # Threshold for whale transactions

    # Transactions per second
    trx_per_sec_x = trx_per_second('x_transactions', date_single_day)
    print(f"X-Chain - Transactions per second: {trx_per_sec_x}")
    trx_per_sec_c = trx_per_second('c_transactions', date_single_day)
    print(f"C-Chain - Transactions per second: {trx_per_sec_c}")
    trx_per_sec_p = trx_per_second('p_transactions', date_single_day)
    print(f"P-Chain - Transactions per second: {trx_per_sec_p}")

    # Transactions per day
    trx_per_day_val_x = trx_per_day('x_transactions', date_single_day)
    print(f"X-Chain - Transactions per day: {trx_per_day_val_x}")
    trx_per_day_val_c = trx_per_day('c_transactions', date_single_day)
    print(f"C-Chain - Transactions per day: {trx_per_day_val_c}")
    trx_per_day_val_p = trx_per_day('p_transactions', date_single_day)
    print(f"P-Chain - Transactions per day: {trx_per_day_val_p}")

    # Total transactions
    total_transactions_x = total_trxs('x_transactions', date_single_day)
    print(f"X-Chain - Total transactions: {total_transactions_x}")
    total_transactions_c = total_trxs('c_transactions', date_single_day)
    print(f"C-Chain - Total transactions: {total_transactions_c}")
    total_transactions_p = total_trxs('p_transactions', date_single_day)
    print(f"P-Chain - Total transactions: {total_transactions_p}")

    # Average Transaction Amount
    avg_transaction_amount_x = avg_trx_amount('x_consumed_utxos', date_single_day)
    print(f"X-Chain - Average Transaction Amount: {avg_transaction_amount_x}")
    avg_transaction_amount_c = avg_trx_amount('c_consumed_utxos', date_single_day)
    print(f"X-Chain - Average Transaction Amount: {avg_transaction_amount_c}")
    avg_transaction_amount_p = avg_trx_amount('p_consumed_utxos', date_single_day)
    print(f"X-Chain - Average Transaction Amount: {avg_transaction_amount_p}")

    # Total blocks
    total_blocks_val_x = total_blocks('x_transactions', date_single_day)
    print(f"X-Chain - Total blocks: {total_blocks_val_x}")
    total_blocks_val_c = total_blocks('c_transactions', date_single_day)
    print(f"C-Chain - Total blocks: {total_blocks_val_c}")
    total_blocks_val_p = total_blocks('p_transactions', date_single_day)
    print(f"P-Chain - Total blocks: {total_blocks_val_p}")

    # Average Transactions in a Block on X-Chain
    average_transactions_x = average_tx_per_block('x_transactions', date_single_day)
    print(f"X-Chain - Average Transactions in a Block: {average_transactions_x}")
    average_transactions_c = average_tx_per_block('c_transactions', date_single_day)
    print(f"C-Chain - Average Transactions in a Block: {average_transactions_c}")
    average_transactions_p = average_tx_per_block('p_transactions', date_single_day)
    print(f"P-Chain - Average Transactions in a Block: {average_transactions_p}")
    
    # Average Transactions Per Hour on X-Chain
    avg_transactions_per_hour_x = avg_trxs_per_hour('x_transactions', date_single_day)
    print(f"X-Chain - Average Transactions Per Hour: {avg_transactions_per_hour_x}")
    avg_transactions_per_hour_c = avg_trxs_per_hour('c_transactions', date_single_day)
    print(f"X-Chain - Average Transactions Per Hour: {avg_transactions_per_hour_c}")
    avg_transactions_per_hour_p = avg_trxs_per_hour('p_transactions', date_single_day)
    print(f"X-Chain - Average Transactions Per Hour: {avg_transactions_per_hour_p}")

    #Active Adresses
    active_addresses_x = active_addresses('x_emitted_utxos', 'x_consumed_utxos', date_single_day)
    print(f"X-Chain - Active Addresses: {active_addresses_x}")
    active_addresses_c = active_addresses('c_emitted_utxos', 'c_consumed_utxos', date_single_day)
    print(f"C-Chain - Active Addresses: {active_addresses_c}")
    active_addresses_p = active_addresses('p_emitted_utxos', 'p_consumed_utxos', date_single_day)
    print(f"P-Chain - Active Addresses: {active_addresses_p}")

    # Active Senders
    active_senders_x = active_senders('x_consumed_utxos', date_single_day)
    print(f"X-Chain - Active Senders: {active_senders_x}")
    active_senders_c = active_senders('c_consumed_utxos', date_single_day)
    print(f"C-Chain - Active Senders: {active_senders_c}")
    active_senders_p = active_senders('p_consumed_utxos', date_single_day)
    print(f"P-Chain - Active Senders: {active_senders_p}")

    # Cumulative number of transactions
    cum_trx_x = cumulative_number_of_trx('x_transactions', date_single_day)
    print(f"X-Chain - Cumulative transactions: {cum_trx_x}")
    cum_trx_c = cumulative_number_of_trx('c_transactions', date_single_day)
    print(f"C-Chain - Cumulative transactions: {cum_trx_c}")
    cum_trx_p = cumulative_number_of_trx('p_transactions', date_single_day)
    print(f"P-Chain - Cumulative transactions: {cum_trx_p}")

    # Sum of Emitted UTXO Amounts
    sum_emitted_utxo_amount_x = sum_emitted_utxo_amount('x_emitted_utxos', date_single_day)
    print(f"X-Chain - Sum of Emitted UTXO Amounts: {sum_emitted_utxo_amount_x}")
    sum_emitted_utxo_amount_c = sum_emitted_utxo_amount('c_emitted_utxos', date_single_day)
    print(f"C-Chain - Sum of Emitted UTXO Amounts: {sum_emitted_utxo_amount_c}")
    sum_emitted_utxo_amount_p = sum_emitted_utxo_amount('p_emitted_utxos', date_single_day)
    print(f"P-Chain - Sum of Emitted UTXO Amounts: {sum_emitted_utxo_amount_p}")

    #Average Emmited UTXO Amount
    avg_emmited_utxo_amount_x = avg_emmited_utxo_amount('x_emitted_utxos', date_single_day)
    print(f"X-Chain - Average Transaction Value: {avg_emmited_utxo_amount_x}")
    avg_emmited_utxo_amount_c = avg_emmited_utxo_amount('c_emitted_utxos', date_single_day)
    print(f"C-Chain - Average Transaction Value: {avg_emmited_utxo_amount_c}")
    avg_emmited_utxo_amount_p = avg_emmited_utxo_amount('p_emitted_utxos', date_single_day)
    print(f"P-Chain - Average Transaction Value: {avg_emmited_utxo_amount_p}")

    #Median Emmited UTXO Amount
    median_emmited_utxo_amount_x = median_emmited_utxo_amount('x_emitted_utxos', date_single_day)
    print(f"X-Chain - Median Transaction Value: {median_emmited_utxo_amount_x}")
    median_emmited_utxo_amount_c = median_emmited_utxo_amount('c_emitted_utxos', date_single_day)
    print(f"C-Chain - Median Transaction Value: {median_emmited_utxo_amount_c}")
    median_emmited_utxo_amount_p = median_emmited_utxo_amount('p_emitted_utxos', date_single_day)
    print(f"P-Chain - Median Transaction Value: {median_emmited_utxo_amount_p}")

    # Sum of Consumed UTXO Amounts
    sum_consumed_utxo_amount_x = sum_consumed_utxo_amount('x_consumed_utxos', date_single_day)
    print(f"X-Chain - Sum of Consumed UTXO Amounts: {sum_consumed_utxo_amount_x}")
    sum_consumed_utxo_amount_c = sum_consumed_utxo_amount('c_consumed_utxos', date_single_day)
    print(f"C-Chain - Sum of Consumed UTXO Amounts: {sum_consumed_utxo_amount_c}")
    sum_consumed_utxo_amount_p = sum_consumed_utxo_amount('p_consumed_utxos', date_single_day)
    print(f"P-Chain - Sum of Consumed UTXO Amounts: {sum_consumed_utxo_amount_p}")

    # Average Consumed UTXO Amount
    avg_consumed_utxo_amount_x = avg_consumed_utxo_amount('x_consumed_utxos', date_single_day)
    print(f"X-Chain - Average Consumed UTXO Value: {avg_consumed_utxo_amount_x}")
    avg_consumed_utxo_amount_c = avg_consumed_utxo_amount('c_consumed_utxos', date_single_day)
    print(f"C-Chain - Average Consumed UTXO Value: {avg_consumed_utxo_amount_c}")
    avg_consumed_utxo_amount_p = avg_consumed_utxo_amount('p_consumed_utxos', date_single_day)
    print(f"P-Chain - Average Consumed UTXO Value: {avg_consumed_utxo_amount_p}")

    # Median Consumed UTXO Amount
    median_consumed_utxo_amount_x = median_consumed_utxo_amount('x_consumed_utxos', date_single_day)
    print(f"X-Chain - Median Consumed UTXO Value: {median_consumed_utxo_amount_x}")
    median_consumed_utxo_amount_c = median_consumed_utxo_amount('c_consumed_utxos', date_single_day)
    print(f"C-Chain - Median Consumed UTXO Value: {median_consumed_utxo_amount_c}")
    median_consumed_utxo_amount_p = median_consumed_utxo_amount('p_consumed_utxos', date_single_day)
    print(f"P-Chain - Median Consumed UTXO Value: {median_consumed_utxo_amount_p}")


    #Total Staked Amount - P Chain
    total_staked_p = total_staked_amount('p_transactions', date_single_day)
    print(f"P-Chain - Total Staked Amount: {total_staked_p}")

    #Total Burned Amount - P Chain
    total_burned_p = total_burned_amount('p_transactions', date_single_day)
    print(f"P-Chain - Total Burned Amount: {total_burned_p}")

    # Large Transactions
    large_transactions_x = large_trx('x_emitted_utxos', 'x_consumed_utxos', date_single_day, large_trx_threshold)
    print(f"X-Chain - Large Transactions: {large_transactions_x}")
    large_transactions_c = large_trx('c_emitted_utxos', 'c_consumed_utxos', date_single_day, large_trx_threshold)
    print(f"C-Chain - Large Transactions: {large_transactions_c}")
    large_transactions_p = large_trx('p_emitted_utxos', 'p_consumed_utxos', date_single_day, large_trx_threshold)
    print(f"P-Chain - Large Transactions: {large_transactions_p}")

    # Whale Transactions
    whale_transactions_x = whale_address_activity('x_emitted_utxos', 'x_consumed_utxos', date_single_day, whale_trx_threshold)
    print(f"X-Chain - Whale Transactions: {whale_transactions_x}")
    whale_transactions_c = whale_address_activity('c_emitted_utxos', 'c_consumed_utxos', date_single_day, whale_trx_threshold)
    print(f"C-Chain - Whale Transactions: {whale_transactions_c}")
    whale_transactions_p = whale_address_activity('p_emitted_utxos', 'p_consumed_utxos', date_single_day, whale_trx_threshold)
    print(f"P-Chain - Whale Transactions: {whale_transactions_p}")

    print("---")

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
    # staked_amount = total_staked_amount('x_emitted_utxos', date_range_full)
    # print(f'Total staked amount in X-Chain (date range {date_range_full}): {staked_amount}')


    # print("------------")

    # table = "x_transactions"
    # date = "2023-01-01"  # Specify the date for which you want to calculate the metrics
    # large_trx_threshold = 10000  # Threshold for a large transaction
    # whale_trx_threshold = 50000  # Threshold for whale transactions

    # # Call each function and print the results
    # avg_trx_value_result = avg_trx_value(table, date)
    # print(f"Average Transaction Value on {date}: {avg_trx_value_result}")

    # median_trx_value_result = median_trx_value(table, date)
    # print(f"Median Transaction Value on {date}: {median_trx_value_result}")

    # avg_utxo_value_result = avg_utxo_value('x_emitted_utxos', date)
    # print(f"Average UTXO Value on {date}: {avg_utxo_value_result}")

    # #total_staked_amount_result = total_staked_amount(table, date)
    # #print(f"Total Staked Amount on {date}: {total_staked_amount_result}")

    # #total_burned_amount_result = total_burned_amount(table, date)
    # #print(f"Total Burned Amount on {date}: {total_burned_amount_result}")

    # large_trx_result = large_trx(table, date, large_trx_threshold)
    # print(f"Large Transactions on {date}: {large_trx_result}")

    # whale_address_activity_result = whale_address_activity(table, date, whale_trx_threshold)
    # print(f"Whale Address Activity on {date}: {whale_address_activity_result}")

    # #cross_chain_whale_trx_result = cross_chain_whale_trx(table, date, threshold)
    # #print(f"Cross-Chain Whale Transactions on {date}: {cross_chain_whale_trx_result}")

    # active_addresses_result = active_addresses(table, date)
    # print(f"Active Addresses on {date}: {active_addresses_result}")