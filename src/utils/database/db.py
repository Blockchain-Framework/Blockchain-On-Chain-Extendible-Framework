import psycopg2
from ..logs import Logger

logger = Logger("GodSight")

def connect_database(config):
    try:
        conn = psycopg2.connect(
            dbname=config.db_name, user=config.db_user,
            password=config.db_password, host=config.db_host
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.log_error(f"Database connection failed: {e}")
        return None
    
def test_connection(config):

    try:
        conn = connect_database(config)
        cur = conn.cursor()

        # Execute a query
        cur.execute("SELECT version();")

        # Retrieve query results
        records = cur.fetchone()
        logger.log_info(f"Connected to: {records}")

        # Close cursor and connection
        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        logger.log_error(f"Database connection failed: {e}")
        return None
    except Exception as e:
        logger.log_error(f"Database failed: {e}")
        return None
    
def initialize_database(config):
    try:
        conn = connect_database(config)

        # Read SQL commands from the data.sql file
        with open('data.sql', 'r') as file:
            sql_commands = file.read()

        # Execute SQL commands
        with conn.cursor() as cur:
            cur.execute(sql_commands)
            conn.commit()
        
        logger.log_info("Database initialized successfully.")
        cur.close()
        conn.close()
    except psycopg2.OperationalError as e:
        logger.log_error(f"Database connection failed: {e}")
        return None
    except Exception as e:
        logger.log_error(f"Database failed: {e}")
        return None
