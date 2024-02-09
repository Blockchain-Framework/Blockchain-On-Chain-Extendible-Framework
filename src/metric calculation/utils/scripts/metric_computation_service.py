import pandas as pd
import psycopg2
import sys
import logging
import os
import json

from utils.database.database_service import get_query_results, append_dataframe_to_sql

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
    append_dataframe_to_sql(table, result_df)
    

#ALL CHAINS SPECIFIC
        
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
            # add_data_to_database('trx_per_second', date, blockchain, subchain, count / 86400)
            return count / 86400
        else:
            logging.info("No transactions found for the given date.")
            # add_data_to_database('trx_per_second', date, blockchain, subchain, 0)

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
        # add_data_to_database('trx_per_day', date, blockchain, subchain, results.iloc[0]['count'])
        return results.iloc[0]['count']
    # add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    return None

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
        # add_data_to_database('total_trxs', date, blockchain, subchain, results.iloc[0]['count'])
        return results.iloc[0]['count']
    # add_data_to_database('total_trxs', date, blockchain, subchain, None)
    return None

@key_mapper("total_trx_amount")
def total_trx_amount(blockchain, subchain, date):
    """
    Calculate the total transaction amount in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for total_trx_amount.")
        return None

    # Query for the sum of transaction amounts
    query = f"""
    SELECT SUM(CAST(amount AS NUMERIC)) as total_amount
    FROM {subchain}_consumed_utxos
    WHERE date = '{date}'
    """
    results = execute_query(query)

    if results is not None and not results.empty:
        total_amount = results.iloc[0]['total_amount']

        if total_amount is not None:
            # Insert result into database, assuming you have a similar function for total amounts
            add_data_to_database('total_trx_amount', date, blockchain, subchain, total_amount)
            return total_amount
        else:
            logging.info("No transactions found for the given date.")
            # Insert zero total amount for the date into the database
            add_data_to_database('total_trx_amount', date, blockchain, subchain, 0)
            return 0
    else:
        logging.info("No data found to calculate total transaction amount for the given date.")
        # Insert null total amount for the date into the database
        add_data_to_database('total_trx_amount', date, blockchain, subchain, None)
        return None

@key_mapper("avg_trx_amount")
def avg_trx_amount(blockchain, subchain, date):
    """
    Calculate the average transaction amount in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_trx_amount.")
        return None

    # Query for the sum of transaction amounts and count of transactions
    query = f"""
    SELECT SUM(CAST(amount AS NUMERIC)) as total_amount, COUNT(*) as trx_count
    FROM {subchain}_consumed_utxos
    WHERE date = '{date}'
    """
    results = execute_query(query)

    if results is not None and not results.empty:
        total_amount = results.iloc[0]['total_amount']
        trx_count = results.iloc[0]['trx_count']

        if trx_count > 0:
            avg_amount = total_amount / trx_count
            # add_data_to_database('avg_trx_amount', date, blockchain, subchain, avg_amount)
            return avg_amount
        else:
            logging.info("No transactions found for the given date.")
            # add_data_to_database('avg_trx_amount', date, blockchain, subchain, 0)
            return 0
    # add_data_to_database('avg_trx_amount', date, blockchain, subchain, None)
    return None

@key_mapper("avg_trxs_per_hour")
def avg_trxs_per_hour(blockchain, subchain, date):
    """
    Calculate the average number of transactions per hour for a given blockchain subchain and date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_trxs_per_hour.")
        return None

    # Query for total number of transactions
    trx_count_query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
    trx_results = execute_query(trx_count_query)

    if trx_results is not None and not trx_results.empty:
        count_trxs = trx_results.iloc[0]['count']
        hours_in_day = 24
        avg_trxs_hour = count_trxs / hours_in_day

        # Insert result into database
        # add_data_to_database('avg_trxs_per_hour', date, blockchain, subchain, avg_trxs_hour)

        return avg_trxs_hour
    else:
        logging.info("No transactions found for the given date.")
        
        # Insert zero transactions for the date into the database
        # add_data_to_database('avg_trxs_per_hour', date, blockchain, subchain, 0)

        return 0

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
        # add_data_to_database('trx_per_day', date, blockchain, subchain,  results.iloc[0]['count'])
        return results.iloc[0]['count']
    # add_data_to_database('trx_per_day', date, blockchain, subchain, None)
    # return None

@key_mapper("avg_tx_per_block")
def avg_tx_per_block(blockchain, subchain, date):
    """
    Calculate the average number of transactions per block in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_tx_per_block.")
        return None

    query = f"""
    SELECT AVG(tx_count) as avg_tx_per_block
    FROM (
        SELECT \"blockHash\", COUNT(*) as tx_count
        FROM {subchain}_transactions
        WHERE date = '{date}'
        GROUP BY \"blockHash\"
    ) as block_transactions
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        avg_tx_block = results.iloc[0]['avg_tx_per_block']

        # Insert result into database
        # add_data_to_database('avg_tx_per_block', date, blockchain, subchain, avg_tx_block)

        return avg_tx_block
    else:
        logging.info("No transactions found for the given date.")

        # Insert zero transactions for the date into the database
        # add_data_to_database('avg_tx_per_block', date, blockchain, subchain, None)

        return None

@key_mapper("active_addresses")
def active_addresses(blockchain, subchain, date):
    """
    Calculate the number of unique addresses that have been active (either sending or receiving) in a given blockchain subchain on a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for active_addresses.")
        return None

    # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
    query = f"""
    SELECT COUNT(DISTINCT addresses) FROM (
        SELECT addresses FROM {subchain}_emitted_utxos WHERE date = '{date}'
        UNION
        SELECT addresses FROM {subchain}_consumed_utxos WHERE date = '{date}'
    ) AS active_addresses
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        active_addrs_count = results.iloc[0]['count']

        # Insert result into database
        # add_data_to_database('active_addresses', date, blockchain, subchain, active_addrs_count)

        return active_addrs_count
    else:
        logging.info("No active addresses found for the given date.")

        # Insert zero active addresses for the date into the database
        # add_data_to_database('active_addresses', date, blockchain, subchain, 0)

        return 0

@key_mapper("active_senders")
def active_senders(blockchain, subchain, date):
    """
    Calculate the number of unique active senders (addresses) on a given date in a specified blockchain subchain.
    Active senders are defined as addresses that have sent (consumed) on the specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for active_senders.")
        return None

    # Assuming 'consumed_table' translates to a sender-focused part of the subchain transactions
    query = f"""
    SELECT COUNT(DISTINCT addresses) as active_senders_count
    FROM {subchain}_consumed_utxos
    WHERE date = '{date}'
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        active_senders_count = results.iloc[0]['active_senders_count']

        # Insert result into database
        # add_data_to_database('active_senders', date, blockchain, subchain, active_senders_count)

        return active_senders_count
    else:
        logging.info("No active senders found for the given date.")

        # Insert zero active senders for the date into the database
        # add_data_to_database('active_senders', date, blockchain, subchain, 0)

        return 0

@key_mapper("sum_emitted_utxo_amount")
def sum_emitted_utxo_amount(blockchain, subchain, date):
    """
    Calculate the sum of emitted UTXO amounts in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for sum_emitted_utxo_amount.")
        return None

    query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {subchain}_emitted_utxos WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        emitted_utxo_sum = results.iloc[0]['sum']

        # Insert result into database
        # add_data_to_database('sum_emitted_utxo_amount', date, blockchain, subchain, emitted_utxo_sum)

        return emitted_utxo_sum
    else:
        logging.warning(f"No data found for sum of emitted UTXO amounts on {date} in {subchain}.")
        
        # Insert null value for the date into the database
        # add_data_to_database('sum_emitted_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("avg_emmited_utxo_amount")
def avg_emmited_utxo_amount(blockchain, subchain, date):
    """
    Calculate the average transaction value in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_emmited_utxo_amount.")
        return None

    query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {subchain}_emitted_utxos WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        avg_utxo_amount = results.iloc[0]['avg']

        # Insert result into database
        # add_data_to_database('avg_emmited_utxo_amount', date, blockchain, subchain, avg_utxo_amount)

        return avg_utxo_amount
    else:
        logging.warning(f"No data found for average transaction value on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('avg_emmited_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("median_emmited_utxo_amount")
def median_emmited_utxo_amount(blockchain, subchain, date):
    """
    Calculate the median transaction value in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for median_emmited_utxo_amount.")
        return None

    query = f"""
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
    FROM {subchain}_emitted_utxos 
    WHERE date = '{date}'
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        median_utxo_amount = results.iloc[0]['percentile_cont']

        # Insert result into database
        # add_data_to_database('median_emmited_utxo_amount', date, blockchain, subchain, median_utxo_amount)

        return median_utxo_amount
    else:
        logging.warning(f"No data found for median transaction value on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('median_emmited_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("sum_consumed_utxo_amount")
def sum_consumed_utxo_amount(blockchain, subchain, date):
    """
    Calculate the sum of consumed UTXO amounts in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for sum_consumed_utxo_amount.")
        return None

    # Assuming 'consumed_table' refers to a table where UTXOs are consumed in the subchain transactions
    query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {subchain}_consumed_utxos WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        consumed_utxo_sum = results.iloc[0]['sum']

        # Insert result into database
        # add_data_to_database('sum_consumed_utxo_amount', date, blockchain, subchain, consumed_utxo_sum)

        return consumed_utxo_sum
    else:
        logging.warning(f"No data found for sum of consumed UTXO amounts on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('sum_consumed_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("avg_consumed_utxo_amount")
def avg_consumed_utxo_amount(blockchain, subchain, date):
    """
    Calculate the average consumed UTXO value in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for avg_consumed_utxo_amount.")
        return None

    # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
    query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {subchain}_consumed_utxos WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        avg_consumed_utxo = results.iloc[0]['avg']

        # Insert result into database
        # add_data_to_database('avg_consumed_utxo_amount', date, blockchain, subchain, avg_consumed_utxo)

        return avg_consumed_utxo
    else:
        logging.warning(f"No data found for average consumed UTXO value on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('avg_consumed_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("median_consumed_utxo_amount")
def median_consumed_utxo_amount(blockchain, subchain, date):
    """
    Calculate the median consumed UTXO value in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for median_consumed_utxo_amount.")
        return None

    # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
    query = f"""
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
    FROM {subchain}_consumed_utxos 
    WHERE date = '{date}'
    """
    results = execute_query(query)
    
    if results is not None and not results.empty:
        median_consumed_utxo = results.iloc[0]['percentile_cont']

        # Insert result into database
        # add_data_to_database('median_consumed_utxo_amount', date, blockchain, subchain, median_consumed_utxo)

        return median_consumed_utxo
    else:
        logging.warning(f"No data found for median consumed UTXO value on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('median_consumed_utxo_amount', date, blockchain, subchain, None)

        return None

@key_mapper("large_trx")
def large_trx(blockchain, subchain, date):
    """
    Calculate the number of large transactions where either the emitted or consumed amount exceeds a certain threshold value
    for a specified blockchain subchain on a given date.
    """
    threshold = 1000000  # Threshold for a large transaction

    if not subchain or not date or threshold is None:
        logging.error("Invalid input parameters for large_trx.")
        return None

    # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
    query = f"""
    WITH emitted AS (
        SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_emitted
        FROM {subchain}_emitted_utxos
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    ),
    consumed AS (
        SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_consumed
        FROM {subchain}_consumed_utxos
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
        large_trx_count = results.iloc[0]['large_transactions_count']

        # Insert result into database
        # add_data_to_database('large_trx', date, blockchain, subchain, large_trx_count)

        return large_trx_count
    else:
        logging.warning(f"No large transactions found on {date} in {subchain} with threshold {threshold}.")

        # Insert null value for the count into the database
        # add_data_to_database('large_trx', date, blockchain, subchain, None)

        return None

@key_mapper("whale_address_activity")
def whale_address_activity(blockchain, subchain, date):
    """
    Calculate the number of whale transactions where either the emitted or consumed amount exceeds a certain threshold value
    for a specified blockchain subchain on a given date.
    """

    threshold = 8000000000000  # Threshold for whale transactions
    
    if not subchain or not date or threshold is None:
        logging.error("Invalid input parameters for whale_address_activity.")
        return None

    # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
    query = f"""
    WITH whale_emitted AS (
        SELECT \"txHash\"
        FROM {subchain}_emitted_utxos
        WHERE date = '{date}'
        GROUP BY \"txHash\"
        HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
    ),
    whale_consumed AS (
        SELECT \"txHash\"
        FROM {subchain}_consumed_utxos
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
        whale_trx_count = results.iloc[0]['whale_transactions_count']

        # Insert result into database
        # add_data_to_database('whale_address_activity', date, blockchain, subchain, whale_trx_count)

        return whale_trx_count
    else:
        logging.warning(f"No whale transactions found on {date} in {subchain} with threshold {threshold}.")

        # Insert null value for the count into the database
        # add_data_to_database('whale_address_activity', date, blockchain, subchain, None)

        return None

def avg_trx_fee():
    pass

#P CHAIN SPECIFIC

@key_mapper("total_staked_amount")
def total_staked_amount(blockchain, subchain, date):
    """
    Calculate the total amount of tokens staked in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for total_staked_amount.")
        return None

    # Assuming 'table' refers to a table that tracks staking transactions in the subchain
    query = f"SELECT SUM(CAST(\"amountStaked\" AS NUMERIC)) FROM {subchain}_transactions WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        total_staked = results.iloc[0]['sum']

        # Insert result into database
        # add_data_to_database('total_staked_amount', date, blockchain, subchain, total_staked)

        return total_staked
    else:
        logging.warning(f"No data found for total staked amount on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('total_staked_amount', date, blockchain, subchain, None)

        return None

@key_mapper("total_burned_amount")
def total_burned_amount(blockchain, subchain, date):
    """
    Calculate the total amount of tokens burned in a given blockchain subchain for a specified date.
    """
    if not subchain or not date:
        logging.error("Invalid input parameters for total_burned_amount.")
        return None

    # Assuming 'table' refers to a table that tracks token burning transactions in the subchain
    query = f"SELECT SUM(CAST(\"amountBurned\" AS NUMERIC)) FROM {subchain}_transactions WHERE date = '{date}'"
    results = execute_query(query)
    
    if results is not None and not results.empty:
        total_burned = results.iloc[0]['sum']

        # Insert result into database
        # add_data_to_database('total_burned_amount', date, blockchain, subchain, total_burned)

        return total_burned
    else:
        logging.warning(f"No data found for total burned amount on {date} in {subchain}.")

        # Insert null value for the date into the database
        # add_data_to_database('total_burned_amount', date, blockchain, subchain, None)

        return None

@key_mapper("staking_dynamics_index")
def calculate_sdi(blockchain, subchain, date):
    """
    Calculate the Staking Dynamics Index (SDI) for the Avalanche network on a specified date,
    focusing on the p chain for staking-related transactions.
    """
    if not blockchain or not date:
        logging.error("Invalid input parameters for calculate_sdi.")
        return None

    # Assuming `estimatedReward` and `delegationFeePercent` need to be derived or are represented by proxy metrics
    # Here we use placeholders for these values, and you'll need to adjust the queries or calculations based on your actual data structure and availability

    # Placeholder query to sum up the amountStaked and amountBurned from p chain transactions
    query_staking_info = f"""
    SELECT SUM(\"amountStaked\") as total_amount_staked,
           SUM(\"amountBurned\") as total_amount_burned,
           SUM(CAST(CASE WHEN \"estimatedReward\" = '' THEN '0' ELSE \"estimatedReward\" END AS numeric)) as total_estimated_reward,
           AVG(CAST(CASE WHEN \"delegationFeePercent\" = '' THEN '0' ELSE \"delegationFeePercent\" END AS numeric)) as avg_delegation_fee_percent
    FROM {subchain}_transactions
    WHERE date = '{date}'
    """

    result_staking_info = execute_query(query_staking_info)
    
    if result_staking_info is not None and not result_staking_info.empty:
        total_amount_staked = result_staking_info.iloc[0]['total_amount_staked'] if result_staking_info.iloc[0]['total_amount_staked'] else 0
        total_amount_burned = result_staking_info.iloc[0]['total_amount_burned'] if result_staking_info.iloc[0]['total_amount_burned'] else 0
        total_estimated_reward = result_staking_info.iloc[0]['total_estimated_reward'] if result_staking_info.iloc[0]['total_estimated_reward'] else 0
        avg_delegation_fee_percent = result_staking_info.iloc[0]['avg_delegation_fee_percent'] if result_staking_info.iloc[0]['avg_delegation_fee_percent'] else 0

        if total_amount_burned == 0:
            logging.error("Total amount burned is zero, cannot calculate SDI.")
            return None

        # Calculate SDI using the provided formula
        #sdi = (total_amount_staked * total_estimated_reward / total_amount_burned) * (1 - avg_delegation_fee_percent / 100)
        sdi = ((total_amount_staked * total_estimated_reward) / (total_amount_burned)) * (avg_delegation_fee_percent)


        # Insert result into database
        add_data_to_database('metric_results', date, blockchain, subchain, sdi)

        return sdi
    else:
        logging.info("No data found to calculate SDI for the given date.")

        # Insert null SDI for the date into the database
        add_data_to_database('metric_results', date, blockchain, subchain, None)

        return None

@key_mapper("staking_engagement_index")
def calculate_sei(blockchain, subchain, date):
    """
    Calculate the Staking Engagement Index (SEI) for the Avalanche network on a specified date,
    focusing on the p chain for staking-related transactions. Treats 'estimatedReward' values
    that are empty strings as 0.
    """
    if not blockchain or not date:
        logging.error("Invalid input parameters for calculate_sei.")
        return None

    # Adjust the query to handle empty 'estimatedReward' as 0 using COALESCE and NULLIF
    query_staking_engagement = f"""
    SELECT 
        SUM(COALESCE(NULLIF("estimatedReward", '')::numeric, 0)) AS total_estimated_reward,
        SUM("amountStaked") AS total_amount_staked
    FROM {subchain}_transactions
    WHERE date = '{date}'
    """

    result_staking_engagement = execute_query(query_staking_engagement)
    
    if result_staking_engagement is not None and not result_staking_engagement.empty:
        total_estimated_reward = result_staking_engagement.iloc[0]['total_estimated_reward'] if result_staking_engagement.iloc[0]['total_estimated_reward'] else 0
        total_amount_staked = result_staking_engagement.iloc[0]['total_amount_staked'] if result_staking_engagement.iloc[0]['total_amount_staked'] else 0

        if total_amount_staked == 0:
            logging.error("Total amount staked is zero, cannot calculate SEI.")
            return None

        sei = total_estimated_reward / total_amount_staked if total_amount_staked else 0  # Ensure division by zero is handled

        # Insert result into database
        add_data_to_database('metric_results', date, blockchain, subchain, sei)

        return sei
    else:
        logging.info(f"No data found to calculate SEI for the given date: {date}.")

        # Insert null SEI for the date into the database
        add_data_to_database('metric_results', date, blockchain, subchain, None)

        return None


#C CHAIN SPECIFIC

def cummilative_number_of_contract_deployed():
    pass

def contract_calls():
    pass

def token_transfers():
    pass

def contract_creations():
    pass

@key_mapper("interchain_transactional_coherence")
def calculate_itc(blockchain, subchain, date):
    """
    Calculate the Interchain Transactional Coherence (ITC) for the Avalanche network on a specified date,
    focusing on c and p chains for cross-chain transactions.
    """
    if not blockchain or not date:
        logging.error("Invalid input parameters for calculate_itc.")
        return None

    # # Query to get the total value of cross-chain transactions from c and p chains
    # query_cross_chain = f"""
    # SELECT SUM((amountCreated::jsonb ->> 'Avalanche')::numeric) as total_cross_chain_value
    # FROM (
    #     SELECT amountCreated FROM c_transactions WHERE date = '{date}' AND sourceChain IS NOT NULL AND destinationChain IS NOT NULL
    #     UNION ALL
    #     SELECT amountCreated FROM p_transactions WHERE date = '{date}' AND sourceChain IS NOT NULL AND destinationChain IS NOT NULL
    # ) AS cross_chain_transactions
    # """

    # Query to get the total value of cross-chain transactions
    query_cross_chain = f"""
    SELECT SUM((\"amountCreated\"::jsonb ->> 'Avalanche')::numeric) as total_cross_chain_value
    FROM {subchain}_transactions
    WHERE date = '{date}' AND \"sourceChain\" IS NOT NULL AND \"destinationChain\" IS NOT NULL
    """

    # Query to get the total transaction value from all chains (x, c, p)
    query_total_value = f"""
    SELECT SUM((\"amountCreated\"::jsonb ->> 'Avalanche')::numeric) as total_transaction_value
    FROM (
        SELECT \"amountCreated\" FROM x_transactions WHERE date = '{date}'
        UNION ALL
        SELECT \"amountCreated\" FROM c_transactions WHERE date = '{date}'
    ) AS all_transactions
    """

    result_cross_chain = execute_query(query_cross_chain)
    result_total_value = execute_query(query_total_value)
    
    if result_cross_chain is not None and not result_cross_chain.empty and result_total_value is not None and not result_total_value.empty:
        total_cross_chain_value = result_cross_chain.iloc[0]['total_cross_chain_value'] if result_cross_chain.iloc[0]['total_cross_chain_value'] else 0
        total_transaction_value = result_total_value.iloc[0]['total_transaction_value'] if result_total_value.iloc[0]['total_transaction_value'] else 0
        
        if total_transaction_value == 0:
            logging.error("Total transaction value is zero, cannot calculate ITC.")
            return None

        itc = total_cross_chain_value / total_transaction_value if total_transaction_value else None

        # Insert result into database
        add_data_to_database('metric_results', date, blockchain, subchain, itc)

        return itc
    else:
        logging.info("No data found to calculate ITC for the given date.")

        # Insert null ITC for the date into the database
        add_data_to_database('metric_results', date, blockchain, subchain, None)

        return None

@key_mapper("interchain_liquidity_ratio")
def calculate_ilr(blockchain, subchain, date):
    """
    Calculate the Interchain Liquidity Ratio (ILR) for the Avalanche network on a specified date.
    Correctly handles text fields containing JSON representations by converting them to JSONB before extraction.
    """
    if not date:
        logging.error("Invalid input parameter for date.")
        return None

    # Adjusted queries to first cast text fields to JSONB before extracting 'Avalanche' values
    query_interchain_value = f"""
    SELECT 
        SUM((CAST(CAST(\"amountUnlocked\" AS JSONB)->>'Avalanche' AS NUMERIC) + 
        CAST(CAST(\"amountCreated\" AS JSONB)->>'Avalanche' AS NUMERIC))) AS total_interchain_value
    FROM {subchain}_transactions
    WHERE date = '{date}' AND \"sourceChain\" IS NOT NULL AND \"destinationChain\" IS NOT NULL
    """

    query_total_created_value = f"""
    SELECT 
        SUM(CAST(CAST(\"amountCreated\" AS JSONB)->>'Avalanche' AS NUMERIC)) AS total_created_value
    FROM (
        SELECT \"amountCreated\" FROM x_transactions WHERE date = '{date}'
        UNION ALL
        SELECT \"amountCreated\" FROM {subchain}_transactions WHERE date = '{date}'
    ) AS created_values
    """

    result_interchain_value = execute_query(query_interchain_value)
    result_total_created_value = execute_query(query_total_created_value)
    
    if result_interchain_value is not None and not result_interchain_value.empty and result_total_created_value is not None and not result_total_created_value.empty:
        total_interchain_value = result_interchain_value.iloc[0]['total_interchain_value'] if result_interchain_value.iloc[0]['total_interchain_value'] else 0
        total_created_value = result_total_created_value.iloc[0]['total_created_value'] if result_total_created_value.iloc[0]['total_created_value'] else 0

        if total_created_value == 0:
            logging.error("Total created value is zero, cannot calculate ILR.")
            return None

        ilr = total_interchain_value / total_created_value if total_created_value else 0  # Ensure division by zero is handled

        # Insert result into database
        add_data_to_database('metric_results', date, blockchain, subchain, ilr)

        return ilr
    else:
        logging.info(f"No data found to calculate ILR for the given date: {date}.")

        # Insert null ILR for the date into the database
        add_data_to_database('metric_results', date, blockchain, subchain, None)

        return None



#X AND C CHAIN SPECIFIC

@key_mapper("network_economic_efficiency")
def calculate_nee(blockchain, subchain, date):
    """
    Calculate the Network Economic Efficiency (NEE) for a given blockchain subchain on a specified date.
    NEE is calculated as the total value transacted divided by the total amount burned on that date,
    where total value transacted is derived from x and c chains, and total amount burned is from p chain.
    """
    if not blockchain or not subchain or not date:
        logging.error("Invalid input parameters for calculate_nee.")
        return None

    # Combine queries to sum up the amountCreated from x and c chains as Total Value Transacted
    # query_transacted = f"""
    # SELECT SUM((\"amountCreated\"::jsonb ->> 'Avalanche')::numeric) as total_value_transacted
    # FROM (
    #     SELECT \"amountCreated\" FROM x_transactions WHERE date = '{date}'
    #     UNION ALL
    #     SELECT \"amountCreated\" FROM c_transactions WHERE date = '{date}'
    # ) AS transacted
    # """

    # Summing up the amountCreated as a proxy for Total Value Transacted
    query_transacted = f"""
    SELECT SUM((\"amountCreated\"::jsonb ->> 'Avalanche')::numeric) as total_value_transacted
    FROM {subchain}_transactions
    WHERE date = '{date}'
    """

    # Query to sum up the amountBurned from p chain as Total Amount Burned
    query_burned = f"""
    SELECT SUM(\"amountBurned\") as total_amount_burned
    FROM p_transactions
    WHERE date = '{date}'
    """

    result_transacted = execute_query(query_transacted)
    result_burned = execute_query(query_burned)
    
    if result_transacted is not None and not result_transacted.empty and result_burned is not None and not result_burned.empty:
        total_value_transacted = result_transacted.iloc[0]['total_value_transacted'] if result_transacted.iloc[0]['total_value_transacted'] else 0
        total_amount_burned = result_burned.iloc[0]['total_amount_burned'] if result_burned.iloc[0]['total_amount_burned'] else 0
        
        if total_amount_burned == 0:
            logging.error("Total amount burned is zero, cannot calculate NEE.")
            return None

        nee = total_value_transacted / total_amount_burned if total_amount_burned else None

        # Insert result into database
        add_data_to_database('metric_results', date, blockchain, subchain, nee)

        return nee
    else:
        logging.info("No data found to calculate NEE for the given date and subchain.")

        # Insert null NEE for the date into the database
        add_data_to_database('metric_results', date, blockchain, subchain, None)

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



if __name__ == "__main__":
    # Define date ranges and thresholds for calculations
    date_single_day = '2024-01-27'
    date_range_full = ('2024-01-20', '2024-01-27')
    large_trx_threshold = 1000000  # Threshold for a large transaction
    whale_trx_threshold = 8000000000000  # Threshold for whale transactions

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
    #staked_amount = total_staked_amount('x_emitted_utxos', date_range_full)
    #print(f'Total staked amount in X-Chain (date range {date_range_full}): {staked_amount}')