from .db import connect_database
from ...logs.log import Logger
from sqlalchemy import MetaData, Table, Column, String, Integer, Float
from sqlalchemy.exc import NoSuchTableError
import psycopg2
from psycopg2 import sql

logger = Logger("GodSight")


def get_all_metrics(config):
    metrics_list = []
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT id FROM metric_table")
                # Fetch all results
                metrics = cur.fetchall()
                # Extract metric names from the query result and add to the list
                metrics_list = [metric[0] for metric in metrics]
    except Exception as e:
        logger.log_error(f"Failed to fetch metrics: {e}")
        raise Exception(f"Failed to fetch metrics: {e}")
    return metrics_list


def get_base_metrics(config, blockchain, subchain):
    metrics_list = []
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT metric_table.id FROM metric_table INNER JOIN chain_metric ON "
                            "metric_table.id=chain_metric.metric_id INNER JOIN blockchain_table ON blockchain_table.id = chain_metric.blockchain_id WHERE blockchain_table.blockchain=%s AND "
                            "blockchain_table.sub_chain=%s AND metric_table.type=%s;", (blockchain, subchain, 'basic',))
                # Fetch all results
                metrics = cur.fetchall()
                # Extract metric names from the query result and add to the list
                metrics_list = [metric[0] for metric in metrics]
    except Exception as e:
        logger.log_error(f"Failed to fetch metrics: {e}")
        raise Exception(f"Failed to fetch metrics: {e}")
    return metrics_list


def create_metric_tables_if_not_exist(metrics_list, config):
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        date DATE NOT NULL,
        blockchain VARCHAR(50) NOT NULL,
        subchain VARCHAR(50) NOT NULL,
        value NUMERIC NOT NULL,
        PRIMARY KEY (date, blockchain, subchain)
    );
    """
    try:
        with connect_database(config) as conn:
            with conn.cursor() as cur:
                for metric in metrics_list:
                    # Format the table name for each metric. Adjust naming convention as necessary.
                    table_name = f"{metric.lower()}"
                    cur.execute(sql.SQL(table_creation_query).format(table_name=sql.Identifier(table_name)))
                conn.commit()  # Commit changes to ensure tables are created.
    except psycopg2.Error as e:
        logger.log_error(f"Error creating metric tables: {e}")
        raise Exception(f"Error creating metric tables: {e}")


def check_metric_last_computed_date(config, blockchain_name, subchain_name, metric_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT date FROM metrics_data WHERE blockchain = %s AND sub_chain = %s AND metric_id = %s ORDER BY date DESC LIMIT 1", (blockchain_name, subchain_name, metric_name,))
            result = cur.fetchone()
            if result:
                return result[0]
    return None

def get_subchain_start_date(config, blockchain_name, subchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT start_date FROM blockchain_table WHERE blockchain = %s AND sub_chain = %s", (blockchain_name, subchain_name,))
            result = cur.fetchone()
            if result:
                return result[0]
    return None

def Is_original_subchain(config, blockchain_name, subchain_name):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT original FROM blockchain_table WHERE blockchain = %s AND sub_chain = %s", (blockchain_name, subchain_name,))
            result = cur.fetchone() is not None
            return result
    return False


def insert_blockchain_metrics(data_list, config):
    conn = connect_database(config)
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Prepare the SQL command
                insert_query = "INSERT INTO metrics_data (date, blockchain, sub_chain, metric_id, value) VALUES (%s, %s, %s, %s, %s)"

                insert_values = [
                    (data['date'], data['blockchain'], data['subchain'], data['metric'], float(data['value']) if data['value'] is not None else 0.0)
                    for data in data_list
                ]

                # Execute the query for multiple inserts
                cur.executemany(insert_query, insert_values)
                conn.commit()
        except Exception as e:
            logger.log_error(f"Failed to insert blockchain metric data: {e}")
            conn.rollback()  # Rollback in case of error
        finally:
            conn.close()


