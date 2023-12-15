import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine

# (1) Daily Transaction Count - X, P, C
def compute_transaction_count(dataframe, date, chain, db_connection_string, table_name = 'daily_transaction_count'):

    # Connect to PostgreSQL Server
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Calculate transaction count
    transaction_count = len(dataframe)

    # Define the table name
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            count INTEGER
        );
        INSERT INTO {table_name} (date, chain_name, count) VALUES (%s, %s, %s)""",
        (date, chain, transaction_count))

    cursor.close()
    conn.close()
    return transaction_count

# Average Transactions Per Block - X
def compute_average_transactions_per_block(dataframe, date, chain, db_connection_string, table_name='average_transactions_per_block'):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Group by blockHash and calculate average transactions per block
    avg_transactions_per_block = dataframe.groupby('blockHash').size().mean()

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            avg_transactions_per_block FLOAT
        );
        INSERT INTO {table_name} (date, chain_name, avg_transactions_per_block) VALUES (%s, %s, %s)""",
                   (date, chain, avg_transactions_per_block))

    cursor.close()
    conn.close()
    return avg_transactions_per_block


# Total Staked Amount - P
def compute_total_staked_amount(dataframe, date, chain, db_connection_string, table_name='total_staked_amount'):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Calculate total staked amount
    total_staked_amount = dataframe['amountStaked'].sum()

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            total_staked_amount FLOAT
        );
        INSERT INTO {table_name} (date, chain_name, total_staked_amount) VALUES (%s, %s, %s)""",
                   (date, chain, total_staked_amount))

    cursor.close()
    conn.close()
    return total_staked_amount

# Total Burned Amount - P
def compute_total_burned_amount(dataframe, date, chain, db_connection_string, table_name='total_burned_amount'):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Calculate total burned amount
    total_burned_amount = dataframe['amountBurned'].sum()

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            total_burned_amount FLOAT
        );
        INSERT INTO {table_name} (date, chain_name, total_burned_amount) VALUES (%s, %s, %s)""",
                   (date, chain, total_burned_amount))

    cursor.close()
    conn.close()
    return total_burned_amount

# Average Transaction Value - C
def compute_average_transaction_value(dataframe, date, chain, db_connection_string, table_name='average_transaction_value'):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Calculate average transaction value
    average_transaction_value = (dataframe['total_input_value'] + dataframe['total_output_value']).mean()

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            average_transaction_value FLOAT
        );
        INSERT INTO {table_name} (date, chain_name, average_transaction_value) VALUES (%s, %s, %s)""",
                   (date, chain, average_transaction_value))

    cursor.close()
    conn.close()
    return average_transaction_value

# Large Transaction Monitoring (Whale Watching) - C
def compute_large_transaction_monitoring(dataframe, date, chain, db_connection_string, table_name='large_transaction_monitoring', large_transaction_threshold=1000000):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Filter large transactions
    large_transactions = dataframe[dataframe['total_output_value'] > large_transaction_threshold]

    # Count of large transactions
    large_transaction_count = len(large_transactions)

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            large_transaction_count INTEGER
        );
        INSERT INTO {table_name} (date, chain_name, large_transaction_count) VALUES (%s, %s, %s)""",
                   (date, chain, large_transaction_count))

    cursor.close()
    conn.close()
    return large_transaction_count

# Cross-Chain Whale Activity (Whale Watching) - C
def compute_cross_chain_whale_activity(dataframe, date, chain, db_connection_string, table_name='cross_chain_whale_activity', large_transaction_threshold=1000000):
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Filter cross-chain large transactions
    cross_chain_large_transactions = dataframe[(dataframe['total_output_value'] > large_transaction_threshold) & (dataframe['sourceChain'] != dataframe['destinationChain'])]

    # Count of cross-chain large transactions
    cross_chain_large_transaction_count = len(cross_chain_large_transactions)

    # Create table and insert data
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date VARCHAR(100),
            chain_name VARCHAR(255),
            cross_chain_large_transaction_count INTEGER
        );
        INSERT INTO {table_name} (date, chain_name, cross_chain_large_transaction_count) VALUES (%s, %s, %s)""",
                   (date, chain, cross_chain_large_transaction_count))

    cursor.close()
    conn.close()
    return cross_chain_large_transaction_count


# (2) Daily Transaction Volume

# (3) Average Transaction Value

# (4) Active Senders

# (5) Active Addresses

# (6) Block Size

# (7) Network Hash Rate (for Proof-of-Work Blockchains)

# (8) Smart Contract Execution Metrics

# (9) Token Transfer Count (for Ethereum-based Tokens)

# (10) Token Transfer Volume (for Ethereum-based Tokens)

# (11) Token Holders (for Ethereum-based Tokens)

# (12) Token Price (for Ethereum-based Tokens)





