import psycopg2
import os
from logs.log import Logger
logger = Logger("GodSight")

def test_connection(connection_string):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(connection_string)

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute("SELECT version();")

        # Retrieve query results
        records = cur.fetchone()
        logger.log_info(f"Connected to: {records}")

        # Close cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        logger.log_error(f"Error: {e}")

if __name__ == "__main__":
    db_connection_string = "postgresql://postgres:root@localhost:5432/onchain"
    test_connection(db_connection_string)
