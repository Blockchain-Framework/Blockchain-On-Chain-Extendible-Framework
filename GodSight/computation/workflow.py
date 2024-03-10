# workflow_manager.py
import sys
import os
import logging
from datetime import datetime, timedelta

from dotenv import load_dotenv
import pandas as pd
import numpy as np
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from .config import Config
from GodSight.computation.utils.database.database_service import get_transactions, get_emitted_utxos, \
    get_consumed_utxos, get_blockchains, get_subchains, get_subchain_metrics, get_chain_basic_metrics, get_general_data, \
    load_model_fields
from GodSight.computation.utils.scripts.utils import log_workflow_status
from GodSight.computation.utils.scripts.metric_calculate_helper import load_metrics, insert_metric_results, \
    load_custom_metrics, calculate_utxo_stats
from GodSight.computation.utils.database.database_service import batch_insert_dataframes
from GodSight.computation.utils.database.services import Is_original_subchain, check_metric_last_computed_date, \
    get_subchain_start_date, insert_blockchain_metrics
from logs.log import Logger

load_dotenv()

local_config = Config()
logger = Logger("GodSight")


class MetricCalculationWorkflowManager:

    def metric_workflow(self, end_date, blockchain, subchain, config):
        global data
        try:
            logger.log_info(f"Computing metrics for {blockchain} subchain {subchain}...")
            # Assuming the environment variable or some config holds the paths
            custom_metric_script_path = f"GodSight/computation/metrics/custom/{blockchain}.py"
            base_metric_script_path = r"GodSight/computation/metrics/base/metrics.py"

            basic_metric_results = []
            custom_metric_results = []

            is_original = Is_original_subchain(config, blockchain, subchain)

            if subchain == 'default' and not is_original:
                return [], []

            # Load metric classes for the specified chain
            custom_metric_blueprints, base_metric_blueprints = load_metrics(custom_metric_script_path,
                                                                            base_metric_script_path, subchain,
                                                                            blockchain, config)

            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Process CustomMetric instances
            for blueprint in custom_metric_blueprints:
                metric_instance = blueprint()

                metric_name = metric_instance.name

                metric_type = metric_instance.transaction_type

                last_computed_date = check_metric_last_computed_date(config, blockchain, subchain, metric_name)

                if last_computed_date is None:
                    start_date = get_subchain_start_date(config, blockchain, subchain)
                else:
                    start_date = last_computed_date

                if end_date < start_date:
                    continue

                current_loop_date = start_date
                while current_loop_date <= end_date:
                    date = current_loop_date.strftime("%Y-%m-%d")

                    if metric_type == 'transaction':

                        # Get the combined data as a DataFrame
                        data = get_general_data(blockchain, subchain, date, config)

                    elif metric_type == 'emitted':
                        data = get_emitted_utxos(blockchain, subchain, date, config)

                    elif metric_type == 'consumed':
                        data = get_consumed_utxos(blockchain, subchain, date, config)

                    else:
                        pass

                    # Calculate the metric
                    metric_value = metric_instance.calculate(data)
                    logger.log_info(
                        f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")

                    # Collect each metric result
                    custom_metric_results.append({
                        'date': date,
                        'blockchain': blockchain,
                        'subchain': subchain,
                        'metric': metric_instance.name,
                        'value': metric_value
                    })

                    current_loop_date += timedelta(days=1)

            # Process BaseMetric instances separately if needed
            for blueprint in base_metric_blueprints:
                metric_instance = blueprint()

                metric_name = metric_instance.name

                last_computed_date = check_metric_last_computed_date(config, blockchain, subchain, metric_name)

                if last_computed_date is None:
                    start_date = get_subchain_start_date(config, blockchain, subchain)
                else:
                    start_date = last_computed_date

                if end_date < start_date:
                    continue

                current_loop_date = start_date
                while current_loop_date <= end_date:
                    date = current_loop_date.strftime("%Y-%m-%d")

                    metric_value = metric_instance.calculate(blockchain, subchain, date, config)  # Example signature
                    # print(metric_instance.name, metric_value)
                    logger.log_info(
                        f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")

                    # Collect each metric result
                    basic_metric_results.append({
                        'date': date,
                        'blockchain': blockchain,
                        'subchain': subchain,
                        'metric': metric_instance.name,
                        'value': metric_value
                    })

                    current_loop_date += timedelta(days=1)

            return basic_metric_results, custom_metric_results

        except Exception as e:
            logger.log_error(f"An error occurred during the workflow for {blockchain} subchain {subchain}: {e}")

    def user_defined_metric_for_whole_blockchain(self, blockchain, subchains, basic_metric_names,
                                                 end_date, config):

        # basic_metric_results = []
        custom_metric_results = []

        custom_metric_script_path = f"GodSight/computation/metrics/custom/{blockchain}.py"

        custom_metric_blueprints = load_custom_metrics(custom_metric_script_path, blockchain, 'default',
                                                                               config)

        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Process CustomMetric instances
        for blueprint in custom_metric_blueprints:
            metric_instance = blueprint()

            metric_name = metric_instance.name

            last_computed_date = check_metric_last_computed_date(config, blockchain, 'default', metric_name)

            if last_computed_date is None:
                start_date = get_subchain_start_date(config, blockchain, 'default')
            else:
                start_date = last_computed_date

            if end_date < start_date:
                continue

            current_loop_date = start_date
            while current_loop_date <= end_date:
                date = current_loop_date.strftime("%Y-%m-%d")

                if metric_instance.transaction_type == "transaction":
                    subchains_data = []
                    for subchain in subchains:
                        print(subchain)
                        sub_trx = get_general_data(blockchain, subchain, date, config)

                        subchains_data.append(sub_trx)

                    trx = pd.concat(subchains_data, axis=0, sort=False).reset_index(drop=True)

                    trx_numerical_cols = trx.select_dtypes(include=[np.number]).columns
                    trx[trx_numerical_cols] = trx[trx_numerical_cols].fillna(0)

                    data = trx

                elif metric_instance.transaction_type == "emitted_utxo":
                    subchains_data = []
                    for subchain in subchains:
                        sub_emit_utxo = get_emitted_utxos(blockchain, subchain, date, config)

                        subchains_data.append(sub_emit_utxo)

                    emit_utxo = pd.concat(subchains_data, axis=0, sort=False).reset_index(drop=True)

                    emit_utxo_numerical_cols = emit_utxo.select_dtypes(include=[np.number]).columns
                    emit_utxo[emit_utxo_numerical_cols] = emit_utxo[emit_utxo_numerical_cols].fillna(0)

                    data = emit_utxo
                elif metric_instance.transaction_type == "consumed_utxo":
                    subchains_data = []
                    for subchain in subchains:
                        sub_consume_utxo = get_consumed_utxos(blockchain, subchain, date, config)

                        subchains_data.append(sub_consume_utxo)

                    consume_utxo = pd.concat(subchains_data, axis=0, sort=False).reset_index(drop=True)

                    consume_utxo_numerical_cols = consume_utxo.select_dtypes(include=[np.number]).columns
                    consume_utxo[consume_utxo_numerical_cols] = consume_utxo[consume_utxo_numerical_cols].fillna(0)

                    data = consume_utxo
                else:
                    logger.log_warning(f"Unknown transaction type for metric: {metric_instance.name}")
                    continue

                # Calculate the metric
                metric_value = metric_instance.calculate(data)  # Pass the correct data
                logger.log_info(
                    f"Calculated {metric_instance.name} for {blockchain} subchain {subchain}: {metric_value}")

                # Collect each metric result
                custom_metric_results.append({
                    'date': date,
                    'blockchain': blockchain,
                    'subchain': 'default',
                    'metric': metric_instance.name,
                    'value': metric_value
                })

                current_loop_date += timedelta(days=1)

        return custom_metric_results

    def run_workflow(self, date=None, config=None):
        if config is None:
            config = local_config
        blockchains = get_blockchains(config)
        if blockchains is not None:
            for blockchain in blockchains['blockchain']:
                all_basic_metrics = []
                all_custom_metrics = []
                subchains = get_subchains(blockchain, config)
                if subchains is not None:
                    for subchain in subchains['sub_chain']:
                        metrics = get_subchain_metrics(blockchain, subchain, config)
                        if metrics is not None:
                            log_workflow_status(blockchain, subchain, 'start', 'metric', None, config)
                            try:
                                basic, custom = self.metric_workflow(date, blockchain, subchain,
                                                                     config)
                                all_basic_metrics.extend(basic)
                                all_custom_metrics.extend(custom)
                            except Exception as e:
                                log_workflow_status(blockchain, subchain, 'fail', 'metric', str(e), config)
                            finally:
                                log_workflow_status(blockchain, subchain, 'success', 'metric', None, config)
                if 'default' not in subchains:
                    all_metric_names = get_chain_basic_metrics(blockchain, config)
                    custom = self.user_defined_metric_for_whole_blockchain(blockchain, all_metric_names,
                                                                           all_basic_metrics,
                                                                           date, config)
                    all_custom_metrics.extend(custom)

                all_metrics = all_basic_metrics + all_custom_metrics

                try:
                    if all_metrics:
                        insert_blockchain_metrics(all_metrics, config)
                except Exception as e:
                    raise (e)


if __name__ == "__main__":
    # TODO: need to check all metric tables exits

    dates = ["2024-01-22", "2024-01-23", "2024-01-24", "2024-01-25", "2024-01-26"]
    # date = "2024-01-21"
    manager = MetricCalculationWorkflowManager()
    for i in dates:
        manager.run_workflow(i)
    # manager.run_workflow(date)
