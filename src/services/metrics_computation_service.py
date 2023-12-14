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





