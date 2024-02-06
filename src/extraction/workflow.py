
# workflow_manager.py
import sys
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import importlib.util


from utils.database.database_service import get_query_results
from utils.scripts.utils.log_utils import log_workflow_status

load_dotenv()

# Ensure the correct paths are included for imports
# sys.path.insert(0, os.environ.get("ROOT_DIRECTORY_LOCAL_PATH"))

class MetricCalculationWorkflowManager:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")

    def load_extract_module(self, module_path):
        spec = importlib.util.spec_from_file_location("metrics_module", module_path)
        metrics_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(metrics_module)
        return metrics_module
    
    def map_functions(self, module_path):
        metrics_module = self.load_extract_module(module_path)
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

    def extract(self, date, blockchain, subchain):
        try:
            self.logger.info(f"Computing metrics for {blockchain} subchain {subchain}...")
            module_path = r"src/extraction/utils/scripts/avalanche/avalanche_data_extraction.py"
            function_map = self.map_functions(module_path)
            
            if subchain in function_map:
                last_day = function_map[subchain](date)
                self.logger.info(f"Extract data for {blockchain} subchain {subchain} last day: {last_day}")
            else:
                self.logger.warning(f"No extraction function mapped for {blockchain} subchain {subchain}")
        
            self.logger.info("Workflow completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during the extraction workflow for {blockchain} subchain {subchain}: {e}")
            raise

    def run_workflow(self, date=None):
        blockchains = self.get_blockchains()
        print("bolockchain",blockchains)
        if blockchains is not None:
            
            for blockchain in blockchains['blockchain']:
                subchains = self.get_subchains(blockchain)
                if subchains is not None:
                    for subchain in subchains['sub_chain']:
                        log_workflow_status(blockchain, subchain, 'start', 'extract', None)
                        try:
                            self.extract(date, blockchain, subchain)
                        except Exception as e:
                            log_workflow_status(blockchain, subchain, 'fail', 'extract', str(e))
                        finally:
                            log_workflow_status(blockchain, subchain, 'completed', 'extract', None)

if __name__ == "__main__":
    date = "2024-01-27"
    manager = MetricCalculationWorkflowManager()
    manager.run_workflow(date)