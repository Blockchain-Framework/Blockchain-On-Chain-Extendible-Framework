# workflow_manager.py
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.blockchain.avalanche.avalanche_data_extraction import extract_avalanche_data
from src.services.data_storage_service import store_data
# from data_processing import process_data

# TO DO : install python-dotenv
# TO DO : Import dotend
# TO DO : load envs

class WorkflowManager:
    def __init__(self):
        # Initialize any required variables, connections, etc.
        self.logger = logging.getLogger(__name__)
        # Update these with your actual file path and database credentials
        
        # TO DO : add following links to env
        self.file_path = "file_store"
        self.db_connection_string = "postgresql://postgres:12345@localhost:5432/onchain"
    
    def run_avalanche_data_workflow(self):
        """
        Orchestrates the workflow for extracting, processing, and storing Avalanche blockchain data.
        """
        
        # TO DO : get last day which data stored
        try:
            # Step 1: Extract data
            self.logger.info("Extracting Avalanche data...")
            avalanche_X_data,avalanche_C_data = extract_avalanche_data()

            if avalanche_X_data.empty or avalanche_C_data.empty:
                self.logger.info("No data extracted.")
                return

            # # Step 2: Process data
            # self.logger.info("Processing data...")
            # processed_data = process_data(avalanche_data)

            # Step 3: Store data
            self.logger.info("Storing data...")
            store_data(avalanche_X_data, self.file_path+"/x_file.tsv.gz", 'x_avalanche_data', self.db_connection_string)
            store_data(avalanche_C_data, self.file_path+"/c_file.tsv.gz", 'c_avalanche_data', self.db_connection_string)
            # store_data(avalanche_C_data, self.file_path+"/file.tsv.gz", 'p_avalanche_data', self.db_connection_string)
            
            # TO DO : Metric computations
            
            self.logger.info("Workflow completed successfully.")

        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            # Handle or raise the exception as per your error handling policy

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set up basic logging configuration
    manager = WorkflowManager()
    manager.run_avalanche_data_workflow()
    
