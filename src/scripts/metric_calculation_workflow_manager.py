
# workflow_manager.py
import sys
import os
import logging
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pandas as pd
import pytz
from sqlalchemy import create_engine
import importlib.util

load_dotenv()

# Ensure the correct paths are included for imports
sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from src.blockchain.avalanche.avalanche_data_extraction import extract_x_chain_data, extract_c_chain_data, extract_p_chain_data
from src.services.data_storage_service import append_dataframe_to_sql, set_last_transaction_data
from src.services.metrics_computation_service import (
    trx_per_second,
    trx_per_day,
    avg_trx_per_block,
    total_trxs,
    total_blocks,
    avg_utxo_value,
    large_trx,
    whale_address_activity
)


# def load_module_from_path(path):
#     spec = importlib.util.spec_from_file_location("util", path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# # Path to metrics_module.py
# module_path = '/path/to/metrics_module.py'
# metrics_module = load_module_from_path(module_path)


def calculate_metrics(date_single_day, blockchain, subchain, metrics):
    # Define date ranges and thresholds for calculations
    large_trx_threshold = 10000  # Threshold for a large transaction
    whale_trx_threshold = 50000  # Threshold for whale transactions

    # Map of chain types to their transaction tables
    chain_tables = {
        'X': 'x_transactions',
        'C': 'c_transactions',
        'P': 'p_transactions'
        # Add other chains and their corresponding tables here
    }
    input_utxo ={
        'X': 'x_utxo',
        'C': 'c_utxo',
        'P': 'p_utxo'
    }
    
    output_utxo = {
        
    }
    
    # Check if the chain is valid
    if subchain not in chain_tables:
        print(f"Invalid chain type: {subchain}")
        return

    transaction_table = chain_tables[subchain]

    # Map of metric names to their functions
    metric_functions = {
        'trx_per_second': lambda: trx_per_second(transaction_table, date_single_day),
        'trx_per_day': lambda: trx_per_day(transaction_table, date_single_day),
        'avg_trx_per_block': lambda: avg_trx_per_block(transaction_table, date_single_day),
        'total_trxs': lambda: total_trxs(transaction_table),
        'total_blocks': lambda: total_blocks(transaction_table),
        # 'large_trx': lambda: large_trx(transaction_table, date_range_full, large_trx_threshold),
        # 'whale_address_activity': lambda: whale_address_activity(transaction_table, date_range_full, whale_trx_threshold)
        # Add other metrics and their corresponding functions here
    }

    # DataFrame to store all the results
    results_df = pd.DataFrame()

    # Calculate specified metrics and store in DataFrame
    for metric in metrics:
        if metric in metric_functions:
            result = metric_functions[metric]()
            print(f"{metric}: {result}")
            
            # Append result to DataFrame
            result_row = pd.DataFrame({
                'date': [date_single_day],
                'blockchain': [blockchain],
                'subchain': [subchain],
                'metric': [metric],
                'value': [result]
            })
            results_df = pd.concat([results_df, result_row])

        else:
            print(f"Invalid metric: {metric}")

    # Convert 'date' to datetime and store DataFrame in SQL
    if not results_df.empty:
        results_df['date'] = pd.to_datetime(results_df['date'])
        append_dataframe_to_sql('metrics_table', results_df)
    else:
        print("No metrics calculated.")


# class MetricCalculationWorkflowManager:

#     def __init__(self):
#         self.logger = logging.getLogger(__name__)
#         self.file_path = "file_store"
#         self.db_connection_string = os.environ.get("DATABASE_CONNECTION")

#     def metric_workflow(self, date, blockchain, subchain):
#         try:
#             # Compute metrics
#             self.logger.info(f"Computing metrics for subchain {subchain}...")
#             metrics = ['trx_per_second', 'trx_per_day', 'avg_trx_per_block', 'total_trxs', 'total_blocks']

#             calculate_metrics(date, blockchain, subchain, metrics)
#             self.logger.info("Workflow completed successfully.")

#         except Exception as e:
#             self.logger.error(f"An error occurred during the workflow for subchain {subchain}: {e}")

#     def run_workflow(self, date=None, blockchain = None, subchains=None):
        
#         if subchains is None:
#             subchains = [blockchain]

#         # Define valid subchains
#         valid_subchains = ["X", "C", "P"]

#         if subchains:
#             for subchain in subchains:
#                 if subchain in valid_subchains:
#                     self.metric_workflow(date, blockchain, subchain)
#                 else:
#                     self.logger.error(f"Unsupported subchain type: {subchain}")
#         else:
#             # Run workflow for all valid subchains
#             for subchain in valid_subchains:
#                 self.metric_workflow(date, blockchain, subchain)



class MetricCalculationWorkflowManager:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")

    def load_metrics_module(self, module_path):
        spec = importlib.util.spec_from_file_location("metrics_module", module_path)
        metrics_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(metrics_module)
        return metrics_module

    def map_functions(self, module_path):
        metrics_module = self.load_metrics_module(module_path)
        function_map = {}
        for attr_name in dir(metrics_module):
            attr = getattr(metrics_module, attr_name)
            if callable(attr) and hasattr(attr, '_key'):
                function_map[attr._key] = attr
        return function_map
    
    def get_blockchains(self):
        query = "SELECT DISTINCT blockchain FROM blockchain_table;"
        return get_query_results(query, self.db_connection_string)

    def get_subchains(self, blockchain):
        query = f"SELECT sub_chain FROM blockchain_table WHERE blockchain = '{blockchain}';"
        return get_query_results(query, self.db_connection_string)

    def get_metrics(self, blockchain, subchain):
        query = f"""
        SELECT m.metric_name 
        FROM metric_table m 
        JOIN chain_metric cm ON m.metric_name = cm.metric_name 
        JOIN blockchain_table b ON cm.blockchain_id = b.id 
        WHERE b.blockchain = '{blockchain}' AND b.sub_chain = '{subchain}';
        """
        return get_query_results(query, self.db_connection_string)

    def metric_workflow(self, date, blockchain, subchain, metrics):
        try:
            self.logger.info(f"Computing metrics for {blockchain} subchain {subchain}...")
            module_path = 'src\scripts\metric_calculation_workflow_manager.py'
            function_map = self.map_functions(module_path)
            
            for metric in metrics:
                if metric in function_map:
                    metric_value = function_map[metric](blockchain, subchain, date)
                    self.logger.info(f"Calculated {metric} for {blockchain} subchain {subchain}: {metric_value}")
                else:
                    self.logger.warning(f"No function mapped for metric: {metric}")
            
            self.logger.info("Workflow completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow for {blockchain} subchain {subchain}: {e}")
            #TODO : trow error

    def run_workflow(self, date=None):
        blockchains = self.get_blockchains()
        if blockchains is not None:
            for blockchain in blockchains['blockchain']:
                subchains = self.get_subchains(blockchain)
                if subchains is not None:
                    for subchain in subchains['sub_chain']:
                        metrics = self.get_metrics(blockchain, subchain)
                        if metrics is not None:
                            # TODO : Add inser query for workflow meta table = values(chain,subchain, status=start, task=metric, error=none)
                            try:
                                self.metric_workflow(date, blockchain, subchain, metrics['metric_name'].tolist())
                            except Exception as e:
                                # TODO : Add inser query for workflow meta table = values(chain,subchain, status=fail, task=metric, error=e)
                                pass
                            finally:
                                # TODO : Add inser query for workflow meta table = values(chain,subchain, status=completed, task=metric, error=none)
                                pass
                            

def get_query_results(query, database_connection):
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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

if __name__ == "__main__":
    # dates = ["2024-01-19", "2024-01-20", "2024-01-21", "2024-01-22", "2024-01-23", "2024-01-24", "2024-01-25", "2024-01-26"]
    date = "2024-01-21"
    manager = MetricCalculationWorkflowManager()

    # for date in dates:
    #     print(date)
    #     # manager.run_workflow(date, "Avalanche", ["X"])
    #     manager.run_workflow(date)
    
    manager.run_workflow(date)