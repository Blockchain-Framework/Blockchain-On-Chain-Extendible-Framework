import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def store_data(dataframe, file_path, data_base, db_connection_string):
    # TO DO : Store date vise
    # Store as .tsv.gz
    dataframe.to_csv(file_path, sep='\t', index=False, compression='gzip')
    
    # Connect to PostgreSQL and create database and table if not exists
    create_database_and_table(db_connection_string)
    print("Database created successfully")
    # Store to PostgreSQL
    engine = create_engine(db_connection_string)
    dataframe.to_sql(data_base, engine, if_exists='replace', index=False)

def create_database_and_table(db_connection_string):
    # Extracting the database name from the connection string
    db_name = db_connection_string.split('/')[-1]

    # Connect to PostgreSQL Server
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create database if it does not exist
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name}")

    # Connect to the database
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create table if it does not exist
    # TO DO : work flow meta table (task, blockchain date)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS x_avalanche_data (
            txHash TEXT,
            blockHash TEXT,
            timestamp BIGINT,
            value NUMERIC,
            blockHeight INT,
            txType TEXT,
            memo TEXT,
            chainFormat TEXT
            -- Add other fields as necessary
        );
        CREATE TABLE c_avalanche_data (
            txHash VARCHAR(255) NOT NULL,
            blockHash VARCHAR(255) NOT NULL,
            timestamp BIGINT,
            value NUMERIC,
            blockHeight INT,
            txType VARCHAR(100),
            sourceChain VARCHAR(255),
            destinationChain VARCHAR(255),
            memo TEXT,
            total_input_value NUMERIC,
            total_output_value NUMERIC,
            PRIMARY KEY (txHash)
        );
    """)

    # Close connection
    cursor.close()
    conn.close()
