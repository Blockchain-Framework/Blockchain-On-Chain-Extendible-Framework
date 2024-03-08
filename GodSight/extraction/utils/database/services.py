from .db import connect_database
from GodSight.extraction.logs.log import Logger
from sqlalchemy import MetaData, Table, Column, String, Integer, Float
from sqlalchemy.exc import NoSuchTableError
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

import pandas as pd

logger = Logger("GodSight")


def check_blockchain_exists(config, blockchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM blockchain_table WHERE blockchain = %s", (blockchain_name,))
            result = cur.fetchone() is not None
            return result
    return False


def get_blockchains(config):
    blockchains = []
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT blockchain FROM blockchain_table")
                blockchains = cur.fetchall()
                blockchains = [blockchain[0] for blockchain in blockchains]
    except Exception as e:
        logger.log_error(f"Failed to fetch blockchains: {e}")
        raise Exception(f"Failed to fetch blockchains: {e}")
    return blockchains


def create_extraction_tables_if_missing(config, subchains):
    logger.log_info(f"Check extraction tables for subchains: {subchains}")
    # SQL templates for creating transaction and UTXO tables with a date column
    transaction_table_sql = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "txHash" TEXT PRIMARY KEY,
        "blockHash" TEXT,
        "timestamp" BIGINT,  -- Adjusted to BIGINT to store UNIX timestamp
        "blockHeight" INTEGER,
        "txType" TEXT,
        "memo" TEXT,
        "chainFormat" TEXT,
        "amountUnlocked" JSONB,  -- Assuming JSON storage for amountUnlocked
        "amountCreated" JSONB,   -- Assuming JSON storage for amountCreated
        "sourceChain" TEXT,
        "destinationChain" TEXT,
        "rewardAddresses" TEXT,  -- Adjust as necessary
        "estimatedReward" NUMERIC,
        "startTimestamp" BIGINT,  -- Assuming UNIX timestamp storage
        "endTimestamp" BIGINT,    -- Assuming UNIX timestamp storage
        "delegationFeePercent" NUMERIC,
        "nodeId" TEXT,
        "subnetId" TEXT,
        "value" TEXT,
        "amountStaked" NUMERIC,
        "amountBurned" NUMERIC
    );
    """

    utxo_table_sql = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "utxoId" TEXT,
        "txHash" TEXT,
        "txType" TEXT,
        "addresses" TEXT,
        "value" TEXT,
        "blockHash" TEXT,
        "assetId" TEXT,
        "asset_name" TEXT,
        "asset_symbol" TEXT,
        "denomination" BIGINT,
        "asset_type" TEXT,
        "amount" TEXT
    );
    """

    table_types = ['transactions', 'emitted_utxos', 'consumed_utxos']

    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                for subchain in subchains:
                    for table_type in table_types:
                        # Format the table name for each subchain and table type
                        table_name = f"{subchain}_{table_type}"
                        if table_type == 'transactions':
                            cur.execute(sql.SQL(transaction_table_sql).format(table_name=sql.Identifier(table_name)))
                        else:  # For both emitted and consumed UTXOs
                            cur.execute(sql.SQL(utxo_table_sql).format(table_name=sql.Identifier(table_name)))
                conn.commit()  # Commit the transaction to ensure table creation
    except psycopg2.Error as e:
        logger.log_error(f"Error creating subchain tables: {e}")
        raise Exception(f"Error creating subchain tables: {e}")


def get_subchains(config, blockchain):
    subchains = []
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT DISTINCT sub_chain FROM blockchain_table WHERE blockchain = %s and sub_chain != 'default'",
                    (blockchain,))
                subchains = cur.fetchall()
                subchains = [subchain[0] for subchain in subchains]
    except Exception as e:
        logger.log_error(f"Failed to fetch subchains: {e}")
        raise Exception(f"Failed to fetch subchains: {e}")
    return subchains

def get_chain_id(config, blockchain, subchain):
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM blockchain_table where blockchain = %s and sub_chain = %s",
                            (blockchain, subchain))
                id_result = cur.fetchone()
                if id_result is not None:
                    id_result = id_result[0]
    except Exception as e:
        logger.log_error(f"Failed to fetch id: {e}")
        raise Exception(f"Failed to fetch id: {e}")
    return id_result

def delete_existing_records(chain, current_date, config):
    tables = [f'{chain}_transactions', f'{chain}_emitted_utxos', f'{chain}_consumed_utxos']
    with connect_database(config) as conn:
        with conn.cursor() as cur:
            for table in tables:
                cur.execute(f"DELETE FROM {table} WHERE date = %s", (current_date,))
        conn.commit()

def check_subchain_last_extracted_date(config, blockchain_name, subchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT timestamp FROM workflow_meta_table WHERE chain = %s AND subchain = %s AND task = %s AND status = %s ORDER BY timestamp DESC LIMIT 1", (blockchain_name, subchain_name, 'extraction', 'success',))
            result = cur.fetchone() is not None
            return result
    return False

def get_subchain_start_date(config, blockchain_name, subchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT start_date FROM blockchain_table WHERE blockchain = %s AND sub_chain = %s", (blockchain_name, subchain_name,))
            result = cur.fetchone() is not None
            return result
    return False

def Is_original_subchain(config, blockchain_name, subchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT original FROM blockchain_table WHERE blockchain = %s AND sub_chain = %s", (blockchain_name, subchain_name,))
            result = cur.fetchone() is not None
            return result
    return False

def store_final_trxs(final_trxs, table_name, config):
    """
    Append a list of dictionaries to a PostgreSQL table.

    :param final_trxs: List of dictionaries containing transaction data.
    :param table_name: Name of the table to append data to.
    :param connection_info: Dictionary containing PostgreSQL connection parameters.
    """
    # Establish connection to the PostgreSQL database
    conn = connect_database(config)
    cursor = conn.cursor()

    # Prepare INSERT statement
    # Assumes all dictionaries in final_trxs have the same keys
    columns = final_trxs[0].keys()
    columns_str = ', '.join(columns)  # column names
    values_str = ', '.join([f'%({c})s' for c in columns])  # placeholders
    insert_query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})'

    # Execute batch insert
    try:
        execute_batch(cursor, insert_query, final_trxs)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def load_model_fields(table_name, config):
    conn = connect_database(config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
    fields = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.close()
    return fields


