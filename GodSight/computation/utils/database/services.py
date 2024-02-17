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
                cur.execute("SELECT DISTINCT metric_name FROM metric_table")
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
