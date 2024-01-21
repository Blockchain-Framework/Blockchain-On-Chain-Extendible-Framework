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
    compute_transaction_count,
    compute_average_transactions_per_block,
    compute_total_staked_amount,
    compute_total_burned_amount,
    compute_average_transaction_value,
    compute_large_transaction_monitoring,
    compute_cross_chain_whale_activity
)

class WorkflowManager:
    # Moved the functions dictionary inside the __init__ method to avoid NameError
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