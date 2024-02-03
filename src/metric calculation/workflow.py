
# workflow_manager.py
import sys
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import importlib.util


from utils.database.database_service import get_query_results
from utils.scripts.utils import log_workflow_status

load_dotenv()

# Ensure the correct paths are included for imports
# sys.path.insert(0, os.environ.get("ROOT_DIRECTORY_LOCAL_PATH"))

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
            module_path = r"src/metric calculation/utils/scripts/metric_computation_service.py"
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
            raise

    def run_workflow(self, date=None):
        blockchains = self.get_blockchains()
        print("bolockchain",blockchains)
        if blockchains is not None:
            
            for blockchain in blockchains['blockchain']:
                subchains = self.get_subchains(blockchain)
                if subchains is not None:
                    for subchain in subchains['sub_chain']:
                        metrics = self.get_metrics(blockchain, subchain)
                        if metrics is not None:
                            log_workflow_status(blockchain, subchain, 'start', 'metric', None)
                            try:
                                self.metric_workflow(date, blockchain, subchain, metrics['metric_name'].tolist())
                            except Exception as e:
                                log_workflow_status(blockchain, subchain, 'fail', 'metric', str(e))
                            finally:
                                log_workflow_status(blockchain, subchain, 'completed', 'metric', None)

if __name__ == "__main__":
    dates = ["2024-01-20","2024-01-22","2024-01-23","2024-01-24","2024-01-25","2024-01-26"]
    # date = "2024-01-21"
    manager = MetricCalculationWorkflowManager()
    for i in dates:
        manager.run_workflow(i)
    # manager.run_workflow(date)