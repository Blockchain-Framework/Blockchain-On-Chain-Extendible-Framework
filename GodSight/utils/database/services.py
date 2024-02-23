from tqdm import tqdm
from .db import connect_database
from GodSight.utils.logs.log import Logger

logger = Logger("GodSight")


def check_blockchain_exists(blockchain_name, config):
    conn = connect_database(config)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM blockchain_table WHERE blockchain = %s", (blockchain_name,))
            result = cur.fetchone() is not None
            return result
    return False


def insert_blockchain_metadata(data, config):
    conn = connect_database(config)
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Example insertion, adjust according to your schema
                cur.execute(
                    "INSERT INTO blockchain_table (blockchain, sub_chain, start_date, description) VALUES (%s, %s, "
                    "%s, %s)",
                    data['blockchain'], data['sub_chain'], data['start_date'], data['description'])
                conn.commit()

                # Additional logic for subChains and storing extract.py and mapper.py goes here
        except Exception as e:
            logger.log_error(f"Failed to insert blockchain data: {e}")
            conn.rollback()
            raise Exception(e)


def insert_blockchain_metadata_and_mappings(meta_data, mapping_data, metric_meta, metric_chain_meta, config):
    # Connect to the database using a context manager for better resource management.
    try:
        pbar = tqdm(total=100)
        with connect_database(config) as conn, conn.cursor() as cur:
            # Insert metadata for temp
            insert_stmt_meta = """
                INSERT INTO blockchain_table (id, blockchain, sub_chain, start_date, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            meta_values = [
                (data['id'], data['blockchain'], data['subchain'], data['start_date'], data['description'])
                for data in meta_data
            ]
            cur.executemany(insert_stmt_meta, meta_values)

            pbar.update(20)

            # Insert mappings for each table
            for mapping in mapping_data:
                for table, entries in mapping.items():
                    insert_stmt_mapping = f"""
                        INSERT INTO {table} (blockchain, sub_chain, sourceField, targetField, type, info)
                        VALUES (%(blockchain)s, %(subchain)s, %(sourceField)s, %(targetField)s, %(type)s, %(info)s)
                    """
                    cur.executemany(insert_stmt_mapping, entries)

            pbar.update(30)

            insert_stmt_metric_meta = """
                INSERT INTO metric_table (metric_name, description, category, type)
                VALUES (%(metric_name)s, %(description)s, %(category)s, %(type)s)
            """
            cur.executemany(insert_stmt_metric_meta, metric_meta)

            pbar.update(20)

            insert_stmt_metric = """
                INSERT INTO chain_metric (blockchain_id, blockchain, sub_chain, metric_name)
                VALUES (%(blockchain_id)s, %(blockchain)s, %(sub_chain)s, %(metric_name)s)
            """
            cur.executemany(insert_stmt_metric, metric_chain_meta)

            pbar.update(20)

            conn.commit()

            pbar.update(10)
            pbar.close()

    except Exception as e:
        # Assuming logger is configured and available globally or passed as an argument
        logger.log_error(f"Failed to insert data into database: {e}")
        conn.rollback()
        # Optionally, re-raise the exception or handle it based on your application's requirements
        raise Exception(e)


def delete_blockchain_data(blockchain, config):
    table_names = ['transactions_feature_mappings', 'emitted_utxos_feature_mappings', 'consumed_utxos_feature_mappings']
    try:
        with connect_database(config) as conn, conn.cursor() as cur:
            for mapper_table in table_names:
                delete_stmt_mapping_table = f"""
                    DELETE FROM {mapper_table}
                    WHERE blockchain = %s;
                """
                cur.execute(delete_stmt_mapping_table, (blockchain,))

            delete_stmt_blockchain_metric = """
                                        DELETE FROM chain_metric
                                        WHERE blockchain = %s;
                                    """
            cur.execute(delete_stmt_blockchain_metric, (blockchain,))

            delete_stmt_blockchain = """
                DELETE FROM blockchain_table
                WHERE blockchain = %s;
            """
            cur.execute(delete_stmt_blockchain, (blockchain,))
            
            delete_stmt_metrics = """
                            DELETE FROM metric_table;
                        """
            cur.execute(delete_stmt_metrics)

            conn.commit()
    except Exception as e:
        logger.log_error(f"Failed to delete data: {e}")
        conn.rollback()
        raise


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

