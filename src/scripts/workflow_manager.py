# workflow_manager.py
import sys
import os
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import argparse

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
        
        
    # def run_data_workflow(self):
    #     # Execute function for all blockchains for 7 days
    #     current_date = datetime.now()

    #     # Calculate the date 7 days ago
    #     date_7_days_ago = current_date - timedelta(days=7)

    #     # Format the date as a string in "yyyy-mm-dd" format
    #     start_date = date_7_days_ago.strftime("%Y-%m-%d")
        
    #     #TODO:  fetch last updatede date from database
    #     for blockchain in self.functions:
    #         self.run_data_workflow(start_date, blockchain)
            
    # def run_data_workflow(self, start_date, blockchain):
    #     # Execute function depending on blockchain
    #     if blockchain in self.functions:
    #         self.functions[blockchain](start_date)
    #     else:
    #         self.logger.error("Unsupported blockchain type")

    # def run_data_workflow(self, start_date):
    #     # Execute workflows for all blockchains
    #     for blockchain in self.functions:
    #         self.run_data_workflow(start_date, blockchain)
    
    def run_data_workflow(self, start_date=None, blockchain=None):
        # Set default start date to 7 days ago if not provided
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        if blockchain:
            # Run workflow for a specific blockchain
            if blockchain in self.functions:
                self.functions[blockchain](start_date)
            else:
                self.logger.error(f"Unsupported blockchain type: {blockchain}")
        else:
            # Run workflow for all blockchains
            for blockchain in self.functions:
                self.functions[blockchain](start_date)
              

def parse_args():
    parser = argparse.ArgumentParser(description="Workflow Manager CLI")
    parser.add_argument('--start_date', help='Start date in YYYY-MM-DD format', default=None)
    parser.add_argument('--chain_names', nargs='*', help='List of blockchain names', default=[])
    parser.add_argument('--functions', nargs='*', help='List of functions to run', default=[])

    return parser.parse_args()

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    args = parse_args()

    # Create a WorkflowManager instance
    manager = WorkflowManager()

    # Convert start_date string to datetime object if provided
    start_date = args.start_date
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Use the current date if start_date is not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)
        start_date = start_date.strftime("%Y-%m-%d")

    # Run workflows based on provided arguments
    for chain in args.chain_names or manager.functions.keys():
        if chain in manager.functions:
            if args.functions:
                for func in args.functions:
                    # Add condition to call specific function if required
                    pass
            else:
                manager.run_data_workflow(start_date, chain)
        else:
            logging.error(f"Unsupported blockchain type: {chain}")

if __name__ == "__main__":
    main()
