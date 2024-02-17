
# workflow_manager.py
import sys
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import importlib.util


from utils.database.database_service import get_query_results, append_dataframe_to_sql, batch_insert_dataframes , get_transactions, get_emitted_utxos, get_consumed_utxos
from utils.scripts.utils import log_workflow_status
from utils.scripts.metric_calculate_helper import load_metrics

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
            # Assuming the environment variable or some config holds the paths
            custom_metric_script_path = r"src/metric calculation/utils/scripts/custom_metric_computation.py"
            base_metric_script_path = r"src/metric calculation/utils/scripts/base_metric_computation.py"
            
            # Retrieve the necessary data for custom metric calculations
            trx = get_transactions(blockchain, subchain)
            emit_utxo = get_emitted_utxos(blockchain, subchain)
            consume_utxo = get_consumed_utxos(blockchain, subchain)
            
            # Load metric classes for the specified chain
            custom_metric_blueprints, base_metric_blueprints = load_metrics(custom_metric_script_path, base_metric_script_path, subchain)

            metric_results = []

            # Process CustomMetric instances
            for blueprint in custom_metric_blueprints:
                metric_instance = blueprint()
                if metric_instance.name in metrics:
                    # Determine the correct data to pass based on transaction_type
                    if metric_instance.transaction_type == "transaction":
                        data = trx
                    elif metric_instance.transaction_type == "emitted_utxo":
                        data = emit_utxo
                    elif metric_instance.transaction_type == "consumed_utxo":
                        data = consume_utxo
                    else:
                        self.logger.warning(f"Unknown transaction type for metric: {metric_instance.name}")
                        continue
                    
                    # Calculate the metric
                    metric_value = metric_instance.calculate(data)  # Pass the correct data
                    self.logger.info(f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")
                    
                    # Collect each metric result
                    metric_results.append({
                        'date': date,
                        'blockchain': blockchain,
                        'subchain': subchain,
                        'metric': metric_instance.name,
                        'value': metric_value
                    })

            # Process BaseMetric instances separately if needed
            for blueprint in base_metric_blueprints:
                metric_instance = blueprint()
                if metric_instance.name in metrics:
                    # For BaseMetric, adjust calculation call as needed
                    metric_value = metric_instance.calculate(blockchain, subchain, date)  # Example signature
                    self.logger.info(f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")

                    # Collect each metric result
                    metric_results.append({
                        'date': date,
                        'blockchain': blockchain,
                        'subchain': subchain,
                        'metric': metric_instance.name,
                        'value': metric_value
                    })

            # Convert collected metric results into a DataFrame and proceed as before
            if metric_results:
                metrics_df = pd.DataFrame(metric_results)
                dfs_to_insert = insert_metric_results(metrics_df)
                batch_insert_dataframes(dfs_to_insert)
                self.logger.info("Metric values successfully inserted into their respective tables in a single transaction.")

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

def insert_metric_results(metrics_df):
    # Initialize a list to collect DataFrames for each metric
    dfs_to_insert = []

    for index, row in metrics_df.iterrows():
        # Determine the table name dynamically from the metric name
        table_name = row['metric']
        # Create a DataFrame for the single row to insert
        row_df = pd.DataFrame([row]).drop(columns=['metric'])
        # Add table name as an attribute for later reference
        row_df._table_name = table_name
        # Collect the DataFrame
        dfs_to_insert.append(row_df)

    return dfs_to_insert

if __name__ == "__main__":
    #TODO: need to check all metric tables exits
    
    dates = ["2024-01-20","2024-01-22","2024-01-23","2024-01-24","2024-01-25","2024-01-26"]
    # date = "2024-01-21"
    manager = MetricCalculationWorkflowManager()
    for i in dates:
        manager.run_workflow(i)
    # manager.run_workflow(date)