# workflow_manager.py
import sys
import os
import logging
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()

# Ensure the correct paths are included for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.blockchain.avalanche.avalanche_data_extraction import extract_x_chain_data, extract_c_chain_data, extract_p_chain_data
from src.services.data_storage_service import store_data, get_last_transaction_data, set_last_transaction_data
from src.services.metrics_computation_service import (
    trx_per_second,
    trx_per_day,
    avg_trx_per_block,
    total_trxs,
    total_blocks,
    trx_count,
    cumulative_number_of_trx,
    avg_trx_value,
    median_trx_value,
    avg_utxo_value,
    large_trx,
    whale_address_activity
)


class WorkflowManager:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_path = "file_store"
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")
        self.functions = {"X": self.run_avalanche_x_data_workflow,
                          "C": self.run_avalanche_c_data_workflow,
                          "P": self.run_avalanche_p_data_workflow,
                          "Bitcoin": self.run_bitcoin_data_workflow}

    def run_avalanche_x_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting Avalanche X data...")
            
            last_date = extract_x_chain_data(start_date)
            
            # Store extracted data and update last timestamps
            set_last_transaction_data(self.db_connection_string, "AVALANCHE_X_CHAIN", last_date, "LastTimeStamp")
            
            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_avalanche_c_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting C Avalanche data...")

            last_date = extract_c_chain_data(start_date)
    
            # Store extracted data and update last timestamps
            set_last_transaction_data(self.db_connection_string, "AVALANCHE_C_CHAIN", last_date, "LastTimeStamp")

            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")

    def run_avalanche_p_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting P Avalanche data...")

            last_date = extract_p_chain_data(start_date)

            # Store extracted data and update last timestamps
            set_last_transaction_data(self.db_connection_string, "AVALANCHE_P_CHAIN", last_date, "LastTimeStamp")

            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_bitcoin_data_workflow(self, start_date):
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


def caculate_metrics():
    # Define date ranges and thresholds for calculations
    date_single_day = '2024-01-21'
    date_range_full = ('2024-01-01', '2024-01-21')
    large_trx_threshold = 10000  # Threshold for a large transaction
    whale_trx_threshold = 50000  # Threshold for whale transactions

    # Transactions per second
    trx_per_sec = trx_per_second('x_transactions', date_single_day)
    print(f"Transactions per second: {trx_per_sec}")

    # Transactions per day
    trx_per_day_val = trx_per_day('x_transactions', date_single_day)
    print(f"Transactions per day: {trx_per_day_val}")
    
    # Average transactions per block
    avg_trx_block = avg_trx_per_block('x_transactions', date_single_day)
    print(f"Average transactions per block: {avg_trx_block}")

    # Total transactions
    total_transactions = total_trxs('x_transactions')
    print(f"Total transactions: {total_transactions}")

    # Total blocks
    total_blocks_val = total_blocks('x_transactions')
    print(f"Total blocks: {total_blocks_val}")

    # Number of transactions in a specific date range
    trx_count_val = trx_count('x_transactions', date_range_full)
    print(f"Number of transactions in date range {date_range_full}: {trx_count_val}")

    # Cumulative number of transactions up to a specified date
    cumulative_trx_val = cumulative_number_of_trx('x_transactions', date_single_day)
    print(f"Cumulative number of transactions up to {date_single_day}: {cumulative_trx_val}")

    # Average transaction value in a specific date range
    avg_trx_value_val = avg_trx_value('x_transactions', date_range_full)
    print(f"Average transaction value in date range {date_range_full}: {avg_trx_value_val}")

    # Median transaction value in a specific date range
    median_trx_value_val = median_trx_value('x_transactions', date_range_full)
    print(f"Median transaction value in date range {date_range_full}: {median_trx_value_val}")

    # Average UTXO Value (X-Chain)
    avg_utxo_val_x = avg_utxo_value('x_emitted_utxos', date_range_full)
    print(f"Average UTXO value in X-Chain date range {date_range_full}: {avg_utxo_val_x}")

    # Large Transactions (X-Chain)
    large_trx_val_x = large_trx('x_transactions', date_range_full, large_trx_threshold)
    print(f"Number of large transactions in X-Chain (threshold: {large_trx_threshold}) in date range {date_range_full}: {large_trx_val_x}")

    # Whale Address Activity (X-Chain)
    whale_activity_val_x = whale_address_activity('x_transactions', date_range_full, whale_trx_threshold)
    print(f"Number of whale transactions in X-Chain (threshold: {whale_trx_threshold}) in date range {date_range_full}: {whale_activity_val_x}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run blockchain data workflow.')

    # Optional argument for start date, defaults to 7 days ago
    parser.add_argument('-d', '--date', type=str, help='Start date in yyyy-mm-dd format', default=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))

    # Required argument for the blockchain type
    parser.add_argument('blockchain', choices=['X', 'C', 'P', 'Bitcoin', 'All'], help='Blockchain type to process (X, C, P, Bitcoin, All)')

    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()

    manager = WorkflowManager()
    start_date = args.date

    if args.blockchain == 'All':
        manager.run_data_workflow_for_all(start_date)
    else:
        if args.blockchain in manager.functions:
            manager.functions[args.blockchain](start_date)
        else:
            print(f"Unsupported blockchain type: {args.blockchain}")