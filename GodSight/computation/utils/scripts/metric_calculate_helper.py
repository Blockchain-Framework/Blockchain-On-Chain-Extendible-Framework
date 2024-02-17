import importlib.util
import os
import pandas as pd

from ...utils.model.metric import BaseMetric, CustomMetric

def load_metrics(custom_metric_script_path, base_metric_script_path, target_chain):
    """
    Load metric classes from scripts for a specific chain, including both CustomMetric and BaseMetric classes.
    :param custom_metric_script_path: Path to the Python script containing CustomMetric definitions.
    :param base_metric_script_path: Path to the Python script containing BaseMetric definitions.
    :param target_chain: The specific chain to load metrics for.
    :return: Two lists of metric class instances that belong to the specified chain, one for CustomMetric and one for BaseMetric.
    """
    
    def load_metric_classes(type_, script_path, metric_base_class):
        
        # Load the script as a module
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        metric_instances = []
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, metric_base_class) and attribute is not metric_base_class:
                # Instantiate the class
                metric_instance = attribute()

                if type_ == 'custom' and metric_instance.chain == target_chain:
                    metric_instances.append(attribute)
                else:
                    metric_instances.append(attribute)
        return metric_instances

    # Load CustomMetric and BaseMetric classes from their respective script paths
    custom_metric_instances = load_metric_classes('custom', custom_metric_script_path, CustomMetric)
    base_metric_instances = load_metric_classes('base',base_metric_script_path, BaseMetric)

    return custom_metric_instances, base_metric_instances

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