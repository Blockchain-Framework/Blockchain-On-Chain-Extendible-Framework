
# workflow_manager.py
import sys
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import Config
from utils.database.database_service import get_transactions, get_emitted_utxos, get_consumed_utxos, get_blockchains, get_subchains, get_metrics
from utils.scripts.utils import log_workflow_status
from utils.scripts.metric_calculate_helper import load_metrics, insert_metric_results
from logs.log import Logger

load_dotenv()

config = Config()
logger = Logger("GodSight")

class MetricCalculationWorkflowManager:

    def metric_workflow(self, date, blockchain, subchain, metrics):
        try:
            logger.log_info(f"Computing metrics for {blockchain} subchain {subchain}...")
            # Assuming the environment variable or some config holds the paths
            custom_metric_script_path = r"metrics\custom\Avalanche.py"
            base_metric_script_path = r"metrics\base\Avalanche.py"
            
            # Retrieve the necessary data for custom metric calculations
            trx = get_transactions(blockchain, subchain, date)
            emit_utxo = get_emitted_utxos(blockchain, subchain, date)
            consume_utxo = get_consumed_utxos(blockchain, subchain, date)
            
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
                        logger.log_warning(f"Unknown transaction type for metric: {metric_instance.name}")
                        continue
                    
                    # Calculate the metric
                    metric_value = metric_instance.calculate(data)  # Pass the correct data
                    logger.log_info(f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")
                    
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
                    print(metric_instance.name, metric_value)
                    logger.log_info(f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")

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
                # batch_insert_dataframes(dfs_to_insert)
                logger.log_info("Metric values successfully inserted into their respective tables in a single transaction.")

            logger.log_info("Workflow completed successfully.")

        except Exception as e:
            logger.log_error(f"An error occurred during the workflow for {blockchain} subchain {subchain}: {e}")
            raise
                
                
    def run_workflow(self, date=None):
        blockchains = get_blockchains()
        if blockchains is not None:
            for blockchain in blockchains['blockchain']:
                subchains = get_subchains(blockchain)
                if subchains is not None:
                    for subchain in subchains['sub_chain']:
                        metrics = get_metrics(blockchain, subchain)
                        if metrics is not None:
                            log_workflow_status(blockchain, subchain, 'start', 'metric', None)
                            try:
                                self.metric_workflow(date, blockchain, subchain, metrics['metric_name'].tolist())
                            except Exception as e:
                                log_workflow_status(blockchain, subchain, 'fail', 'metric', str(e))
                            finally:
                                log_workflow_status(blockchain, subchain, 'completed', 'metric', None)


if __name__ == "__main__":
    #TODO: need to check all metric tables exits
     
    dates = ["2024-01-22","2024-01-23","2024-01-24","2024-01-25","2024-01-26"]
    # date = "2024-01-21"
    manager = MetricCalculationWorkflowManager()
    for i in dates:
        manager.run_workflow(i)
    # manager.run_workflow(date)