import pandas as pd
import psycopg2
import numpy
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine, exc
from sqlalchemy.inspection import inspect as sqla_inspect

def convert_dict_to_json(x):
    if isinstance(x, dict) or (isinstance(x, list) and all(isinstance(elem, dict) for elem in x)):
        return json.dumps(x)
    return x

def append_dataframe_to_sql(table_name, df, database_connection = os.environ.get("DATABASE_CONNECTION")):
    """
    Appends a DataFrame to a SQL table, creating the table if it doesn't exist.
    
    :param table_name: Name of the SQL table.
    :param df: DataFrame to be appended.
    :param database_connection: Database connection string.
    """
    for col in df.columns:
        df[col] = df[col].apply(convert_dict_to_json)
    
    try:
        # Create the database engine
        engine = create_engine(database_connection)

        # Create an inspector
        insp = Inspector.from_engine(engine)
        
        # Check if the table exists
        if insp.has_table(table_name):
            # If table exists, append data
            with engine.begin() as connection:  # Start a transaction
                df.to_sql(table_name, connection, if_exists='append', index=False, chunksize=1000)
        else:
            # If table does not exist, create it and append data
            with engine.begin() as connection:  # Start a transaction
                df.to_sql(table_name, connection, if_exists='fail', index=False, chunksize=1000)

    except SQLAlchemyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_query_results(query, database_connection=os.environ.get("DATABASE_CONNECTION")):
    """
    Executes a SQL query and returns the results as a DataFrame.

    :param query: SQL query to be executed.
    :param database_connection: Database connection string.
    :return: DataFrame containing the query results.
    """
    try:
        # Create the database engine
        engine = create_engine(database_connection)

        # Execute the query and fetch the results
        with engine.connect() as connection:
            results = pd.read_sql_query(query, connection)

        return results

    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        
def store_data(dataframe, file_path, data_base, db_connection_string):
    # TO DO : Store date vise
    # Store as .tsv.gz
    
    # dataframe.to_csv(file_path, sep='\t', index=False, compression='gzip')
    
    # Connect to PostgreSQL and create database and table if not exists
    create_database_and_table(db_connection_string)
    print("Database created successfully")
    # Store to PostgreSQL
    engine = create_engine(db_connection_string)
    
    # TO DO:if_exists='append'
    dataframe.to_sql(data_base, engine, if_exists='replace', index=False)
    
def get_last_transaction_data(db_connection_string, blockchain):

    # Connect to PostgreSQL Server
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create database if it does not exist
    cursor.execute(f"SELECT MAX(timestamp) FROM workflow_meta_table WHERE blockchain = '{blockchain}';")

    # Fetch all the rows and print them
    rows = cursor.fetchall()
    if rows:
        cursor.close()
        conn.close()
        return rows[0][0]
    else:
        return None

import psycopg2

def set_last_transaction_data(db_connection_string, blockchain, timestamp, task=""):
    # Convert numpy.int64 to native Python int
    if isinstance(timestamp, numpy.int64):
        timestamp = int(timestamp)

    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = True
    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    query = "INSERT INTO workflow_meta_table (timestamp, task, blockchain) VALUES (%s, %s, %s);"
    
    # Execute the query with parameters
    cursor.execute(query, (timestamp, task, blockchain))
    
    cursor.close()
    conn.close()


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
    # TO DO : work flow meta table (task, blockchain, date)
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
        CREATE TABLE IF NOT EXISTS c_avalanche_data (
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
        CREATE TABLE IF NOT EXISTS workflow_meta_table (
            timestamp BIGINT,
            task VARCHAR(100),
            blockchain VARCHAR(100)
            );
    """)

    # Close connection
    cursor.close()
    conn.close()
