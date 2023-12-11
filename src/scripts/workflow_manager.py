# workflow_manager.py
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.blockchain.avalanche.avalanche_data_extraction import extract_avalanche_data
from src.services.data_storage_service import store_data
# from data_processing import process_data

class WorkflowManager:
    def __init__(self):
        # Initialize any required variables, connections, etc.
        self.logger = logging.getLogger(__name__)
        # Update these with your actual file path and database credentials
        self.file_path = "path/to/your/file.tsv.gz"
        self.db_connection_string = "postgresql://username:password@localhost:5432/yourdbname"
    
    def run_avalanche_data_workflow(self):
        """
        Orchestrates the workflow for extracting, processing, and storing Avalanche blockchain data.
        """
        try:
            # Step 1: Extract data
            self.logger.info("Extracting Avalanche data...")
            avalanche_data = extract_avalanche_data()

            if avalanche_data.empty:
                self.logger.info("No data extracted.")
                return

            # # Step 2: Process data
            # self.logger.info("Processing data...")
            # processed_data = process_data(avalanche_data)

            # Step 3: Store data
            self.logger.info("Storing data...")
            store_data(avalanche_data, self.file_path, self.db_connection_string)

            self.logger.info("Workflow completed successfully.")

        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            # Handle or raise the exception as per your error handling policy

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set up basic logging configuration
    manager = WorkflowManager()
    manager.run_avalanche_data_workflow()
