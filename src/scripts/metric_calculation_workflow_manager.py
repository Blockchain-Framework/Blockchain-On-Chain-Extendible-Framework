
# workflow_manager.py
import sys
import os
import logging
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pandas as pd

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


class MetricCalculationWorkflowManager:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_path = "file_store"
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")
        self.functions = {"X": self.run_avalanche_x_data_workflow,
                          "C": self.run_avalanche_c_data_workflow,
                          "P": self.run_avalanche_p_data_workflow,
                          "Bitcoin": self.run_bitcoin_data_workflow}

    def run_avalanche_x_metric_workflow(self, date):
        try:
            # Compute metrics
            self.logger.info("Computing metrics...")
            metrics = []
            calculate_metrics(date, chain, metrics)
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_avalanche_c_metric_workflow(self, date):
        try:
            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")

    def run_avalanche_p_metric_workflow(self, date):
        try:
            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_bitcoin_metric_workflow(self, date):
        pass
    
    def run_data_workflow(self):
        # Execute function for all blockchains for 7 days
        current_date = datetime.now()

        # Calculate the date 7 days ago
        date_7_days_ago = current_date - timedelta(days=7)

        # Format the date as a string in "yyyy-mm-dd" format
        start_date = date_7_days_ago.strftime("%Y-%m-%d")
        
        #TODO:  fetch last updatede date from database
        for blockchain in self.functions:
            self.run_data_workflow(start_date, blockchain)
            
    def run_data_workflow(self, start_date, blockchain):
        # Execute function depending on blockchain
        if blockchain in self.functions:
            self.functions[blockchain](start_date)
        else:
            self.logger.error("Unsupported blockchain type")

    def run_data_workflow(self, start_date):
        # Execute workflows for all blockchains
        for blockchain in self.functions:
            self.run_data_workflow(start_date, blockchain)

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

    # Check if the chain is valid
    if chain not in chain_tables:
        print(f"Invalid chain type: {chain}")
        return

    transaction_table = chain_tables[chain]

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
                'subchain': [f'{chain}_chain'],
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run blockchain data workflow.')

    # Optional argument for start date, defaults to 7 days ago
    parser.add_argument('-d', '--date', type=str, help='Start date in yyyy-mm-dd format', default=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))

    # Required argument for the blockchain type
    parser.add_argument('blockchain', choices=['X', 'C', 'P', 'Bitcoin', 'All'], help='Blockchain type to process (X, C, P, Bitcoin, All)')

    return parser.parse_args()

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # args = parse_arguments()

    # manager = WorkflowManager()
    # start_date = args.date

    # if args.blockchain == 'All':
    #     manager.run_data_workflow_for_all(start_date)
    # else:
    #     if args.blockchain in manager.functions:
    #         manager.functions[args.blockchain](start_date)
    #     else:
    #         print(f"Unsupported blockchain type: {args.blockchain}")
    
    dates = ["2024-01-19","2024-01-20","2024-01-21","2024-01-22","2024-01-23","2024-01-24","2024-01-25","2024-01-26"]
    chain = 'X'  # Example for X chain
    metrics_to_calculate = ['trx_per_second','trx_per_day', 'avg_trx_per_block', 'total_trxs', 'total_blocks', 'large_trx', 'whale_address_activity']

    for i in dates:
        print(i)
        calculate_metrics(i, ('2024-01-19', '2024-01-26'), chain, metrics_to_calculate)