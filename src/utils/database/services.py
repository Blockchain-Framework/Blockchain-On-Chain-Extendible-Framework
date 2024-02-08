from .db import connect_database
from ..logs import Logger

logger = Logger("GodSight")

def check_blockchain_exists(blockchain_name, config):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM blockchains WHERE name = %s", (blockchain_name,))
            result = cur.fetchone() is not None
            return result
    return False

def insert_blockchain_metadata(data, config):
    conn = connect_database(config)
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Example insertion, adjust according to your schema
                cur.execute("INSERT INTO blockchain_table (blockchain, sub_chain, start_date, description) VALUES (%s, %s, %s, %s)",
                            data['blockchain'], data['sub_chain'], data['start_date'], data['description'])
                conn.commit()
                
                # Additional logic for subChains and storing extract.py and mapper.py goes here
        except Exception as e:
            logger.log_error(f"Failed to insert blockchain data: {e}")
            conn.rollback()
            raise Exception(e)
        
def insert_blockchain_metadata_and_mappings(meta_data, mapping_data, config):
    # Connect to the database using a context manager for better resource management
    try:
        with connect_database(config) as conn, conn.cursor() as cur:
            # Insert metadata for blockchains
            insert_stmt_meta = """
                INSERT INTO blockchain_table (blockchain, sub_chain, start_date, description)
                VALUES (%s, %s, %s, %s)
            """
            meta_values = [
                (data['blockchain'], data['subchain'], data['start_date'], data['description'])
                for data in meta_data
            ]
            cur.executemany(insert_stmt_meta, meta_values)

            # Insert mappings for each table
            for mapping in mapping_data:
                for table, entries in mapping.items():
                    insert_stmt_mapping = f"""
                        INSERT INTO {table} (blockchain, subchain, sourceField, targetField, type, info)
                        VALUES (%(blockchain)s, %(subchain)s, %(sourceField)s, %(targetField)s, %(type)s, %(info)s)
                    """
                    cur.executemany(insert_stmt_mapping, entries)

            conn.commit()

    except Exception as e:
        # Assuming logger is configured and available globally or passed as an argument
        logger.log_error(f"Failed to insert data into database: {e}")
        # Optionally, re-raise the exception or handle it based on your application's requirements
        raise
