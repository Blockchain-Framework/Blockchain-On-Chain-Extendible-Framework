import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine

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

# Daily Transaction Volume

# Average Transaction Value

# Active Addresses

# Block Size

# Network Hash Rate (for Proof-of-Work Blockchains)

# Smart Contract Execution Metrics

# Token Transfer Count (for Ethereum-based Tokens)

# Token Transfer Volume (for Ethereum-based Tokens)

# Token Holders (for Ethereum-based Tokens)

# Token Price (for Ethereum-based Tokens)





