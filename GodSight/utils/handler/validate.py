import uuid
from datetime import datetime
from pathlib import Path
import importlib.util
import os
import sys
import inspect
import pandas as pd

from GodSight.utils.database.services import fetch_model_data
from GodSight.utils.model.config_mapper import model
from GodSight.utils.model.metric import BaseMetric, CustomMetric
from GodSight.utils.handler.http import fetch_transactions
from GodSight.utils.handler.time import convert_to_gmt_timestamp

from GodSight.utils.logs.log import Logger

logger = Logger("GodSight")


def load_module_from_path(module_name, file_path):
    module_dir = os.path.dirname(file_path)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)  # Temporarily add the directory to sys.path
        added_to_sys_path = True
    else:
        added_to_sys_path = False

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if added_to_sys_path:
        sys.path.remove(module_dir)  # Clean up after import

    return module


def get_function(file_path, function_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    function_module = importlib.util.module_from_spec(spec)
    # TODO: check this below line - ERROR:  attempted relative import beyond top-level package
    spec.loader.exec_module(function_module)
    return getattr(function_module, function_name, None)  # Returns None if the function does not exist


def load_config_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    config_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(config_module)
        # Attempt to return the config attribute
        return config_module.config
    except AttributeError:
        # Handle the case where config is not defined
        print(f"No 'config' attribute found in the module loaded from {file_path}.")
        return None  # Or return an empty config dictionary {}, or raise a custom error


def load_functions_from_file(file_path, function_names):
    functions = {}
    for name in function_names:
        func = get_function(file_path, name)
        if func:
            functions[name] = func
        else:
            return None, func
    return functions, ""


def file_exists(file_path):
    """
    Check if a file exists at the given file path using pathlib.

    :param file_path: String, path to the file.
    :return: Boolean, True if the file exists, False otherwise.
    """
    return Path(file_path).exists()


# And specifically for files
def is_file(file_path):
    """
    Check if the path is specifically a file (not a directory).

    :param file_path: String, path to the file.
    :return: Boolean, True if it's a file, False otherwise.
    """
    return Path(file_path).is_file()


def is_python_file(file_path):
    """
    Check if the path is specifically a Python file (not a directory) and has a '.py' extension.

    :param file_path: String, path to the file.
    :return: Boolean, True if it's a Python file, False otherwise.
    """

    path = Path(file_path)
    # print(f"Path: {path}")
    # print(f"Is file: {path.is_file()}")
    # print(f"Suffix: {path.suffix}")

    return path.is_file() and path.suffix == '.py'


def validate_metadata(blockchain_metadata):
    required_keys = ['name', 'description', 'subChains']
    subchain_required_keys = ['name', 'startDate', 'description', 'extract_file', 'mapper_file']

    # Check the presence of top-level required keys
    if not isinstance(blockchain_metadata, dict) or not all(key in blockchain_metadata for key in required_keys):
        return False, "Invalid format. Required keys: ['name', 'description', 'subChains']"

    # Validate each subchain
    for subchain in blockchain_metadata['subChains']:
        # Check the presence of all required subchain keys
        if not all(key in subchain for key in subchain_required_keys):
            missing_keys = [key for key in subchain_required_keys if key not in subchain]
            return False, f"Missing keys in subchain object. Required keys: {missing_keys}"

        # Validate the 'startDate' format
        try:
            datetime.strptime(subchain['startDate'], "%Y-%m-%d")
        except ValueError:
            return False, f"Invalid startDate format for subchain {subchain['name']}. Use YYYY-MM-DD."

    return True, "Metadata is valid."


def validate_extraction_file(relative_path_from_project_root, test_input):
    """
    Validate the extraction function in the specified file.

    :param file_name: Name of the Python file (without '.py') to be validated.
    :param relative_path_from_project_root: Relative path from the project root to the Python file.
    :param test_input: Test input to pass to the extract function.
    :return: Tuple (Boolean indicating whether the validation passed, and an error message if it failed).
    """

    output = None
    extract_func = None

    if not file_exists(relative_path_from_project_root):
        return False, "The 'extract' file is not exist.", output, None

    if not is_python_file(relative_path_from_project_root):
        return False, "The 'extract' file is not a python script.", output, None

    extract_func = get_function(relative_path_from_project_root, 'extract')

    if extract_func is None:
        return False, "The 'extract' file is not containing the 'extract' function.", output, None

    # Test the 'extract' function with the provided input
    try:
        output = extract_func(test_input)
        # Validate the output's structure
        # Check if output is a tuple (or list) of exactly three elements
        if not isinstance(output, (list, tuple)) or len(output) != 3:
            return False, "Invalid output structure. Expected a tuple or list of three elements.", None, None

        # Validate each element in the output
        for element in output:
            if not isinstance(element, (list, tuple)) or not all(isinstance(item, dict) for item in element):
                return False, "Invalid output structure. Each element must be a list or tuple of dictionaries.", None, None

    except Exception as e:
        return False, f"Error executing the 'extract' function: {e}", None, None

    return True, "Validation passed.", output, extract_func


# def validate_mapper_file(relative_path_from_project_root):
#     # file_path = os.path.join(os.getcwd(), relative_path_from_project_root, file_name+'.py')
#
#     mapper_funcs_str = []
#
#     if not file_exists(relative_path_from_project_root):
#         return False, "The 'mapper' file is not exist.", None, []
#
#     if not is_python_file(relative_path_from_project_root):
#         return False, "The 'mapper' file is not a python script.", None, []
#
#     mapper_config = load_config_from_file(relative_path_from_project_root)
#
#     if mapper_config is None:
#         return False, "No 'config' found in the mapper module.", None, []
#
#     if not isinstance(model, dict):
#         raise TypeError("model is expected to be a dictionary.")
#
#     # Validate the config structure against the model
#     for category, mappings in model.items():
#         if category not in mapper_config:
#             return False, f"Missing '{category}' in mapper config.", None, []
#
#         for field, _ in mappings.items():
#             if field not in mapper_config[category]:
#                 return False, f"Missing '{field}' in '{category}'.", None, []
#
#             config_field = mapper_config[category].get(field)
#             if not config_field:
#                 return False, f"Configuration for '{field}' in '{category}' is not defined.", None, []
#
#             if len(config_field) < 2:
#                 return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []
#
#             if config_field[1] == "function":
#                 if len(config_field) < 3:
#                     return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []
#
#                 mapper_funcs_str.append(config_field[2])
#
#     mapper_funcs, msg = load_functions_from_file(relative_path_from_project_root, mapper_funcs_str)
#
#     if mapper_funcs is None:
#         return False, f"'{msg}' is not a function in mapper file.", None, []
#
#     return True, "Mapper validation passed.", mapper_config, mapper_funcs


def validate_mapper_file(relative_path_from_project_root, config):
    mapper_funcs_str = []

    # Define the expected fields for each model
    # trx_fields = [
    #     'txHash', 'blockHash', 'timestamp', 'blockHeight', 'txType', 'memo',
    #     'chainFormat', 'amountUnlocked', 'amountCreated', 'sourceChain',
    #     'destinationChain', 'rewardAddresses', 'estimatedReward',
    #     'startTimestamp', 'endTimestamp', 'delegationFeePercent', 'nodeId',
    #     'subnetId', 'value', 'amountStaked', 'amountBurned'
    # ]
    #
    # utxo_fields = [
    #     'utxoId', 'txHash', 'txType', 'addresses', 'value', 'blockHash',
    #     'assetId', 'asset_name', 'symbol', 'denomination', 'asset_type', 'amount'
    # ]
    #
    # model_fields_mapping = {
    #     'trx_mapping': trx_fields,
    #     'emit_utxo_mapping': utxo_fields,
    #     'consume_utxo_mapping': utxo_fields,
    # }

    model_fields_mapping = fetch_model_data(config)

    # Assuming file_exists and is_python_file are implemented elsewhere
    if not file_exists(relative_path_from_project_root):
        return False, "The 'mapper' file does not exist.", None, []

    if not is_python_file(relative_path_from_project_root):
        return False, "The 'mapper' file is not a python script.", None, []

    # Assuming load_config_from_file is implemented elsewhere
    mapper_config = load_config_from_file(relative_path_from_project_root)

    if mapper_config is None:
        return False, "No 'config' found in the mapper module.", None, []

    if not isinstance(mapper_config, dict):
        return False, "Config is expected to be a dictionary.", None, []

    for mapping_name, expected_fields in model_fields_mapping.items():
        mapping = mapper_config.get(mapping_name)
        if not mapping:
            return False, f"Mapping '{mapping_name}' not found in config.", None, []

        for field, details in mapping.items():
            if len(details) < 2:
                return False, f"Configuration for '{field}' in '{mapping_name}' is not correct.", None, []

            if field not in expected_fields:
                return False, f"Field '{field}' in mapping '{mapping_name}' does not exist in the expected fields list.", None, []

            if details[1] == "function":
                if len(details) < 3:
                    return False, f"Configuration for '{field}' in '{mapping_name}' is missing function details.", None, []
                mapper_funcs_str.append(details[2])

    # Assuming load_functions_from_file is implemented elsewhere
    mapper_funcs, msg = load_functions_from_file(relative_path_from_project_root, mapper_funcs_str)

    if mapper_funcs is None:
        return False, f"Problem loading functions: '{msg}'.", None, []

    return True, "Mapper validation passed.", mapper_config, mapper_funcs


def validate_mapping_with_functions(mapper_config, extracted_data, functions):
    """
    Validates that the extracted data can be correctly mapped using the mapper config
    and functions.

    :param mapper_config: The mapping configuration dictionary.
    :param extracted_data: A sample of the extracted data to validate the mapping.
    :param functions: A dictionary of loaded functions by name.
    :return: Boolean indicating whether the mapping is valid, and an error message if not.
    """

    formatted_all_data = {}

    # print("Length of extracted_data:", len(extracted_data))

    for category, mappings in mapper_config.items():
        # print("Processing category:", category)

        if category == 'trx_mapping':
            data = extracted_data[0]
            # print("Data for trx_mapping:", data)

        elif category == 'emit_utxo_mapping':
            data = extracted_data[1]
            # print("Data for emit_utxo_mapping:", data)

        elif category == 'consume_utxo_mapping':
            data = extracted_data[2]
            # print("Data for consume_utxo_mapping:", data)

        else:
            # print("Invalid category found in mapper config:", category)
            return False, f"Invalid category in mapper config"

        if data:
            test_data = data[:3]
            # print(f"Sample data for {category}:", test_data)
        else:
            # print(f"No data available for {category}, skipping.")
            continue

        format_data_lst = []
        for test in test_data:
            format_data = {}
            for field, mapping_details in mappings.items():
                mapping_field = mapping_details[0]
                mapping_type = mapping_details[1]
                # print(f"Processing field '{field}' with type '{mapping_type}'")

                if (mapping_field not in test) and mapping_type == "feature":
                    format_data[field] = None

                elif mapping_type == "feature":
                    format_data[field] = test[mapping_field]
                    # print(f"Formatted data for field '{field}':", format_data[field])

                elif mapping_type == "function":
                    function_name = mapping_details[2]
                    if function_name not in functions:
                        return False, f"Function '{function_name}' required for mapping '{field}' is not loaded."

                    try:
                        # Assuming the functions take the field value and return a processed value
                        result = functions[function_name](test)
                        format_data[field] = result
                        # print(f"Result from function '{function_name}' for field '{field}':", result)

                    except Exception as e:
                        # print(f"Error applying function '{function_name}' to field '{field}': {e}")
                        return False, f"Error applying function '{function_name}' to field '{field}': {e}"

            format_data_lst.append(format_data)

        if category == 'trx_mapping':
            formatted_all_data['transaction'] = pd.DataFrame(format_data_lst)

        elif category == 'emit_utxo_mapping':
            formatted_all_data['emitted_utxo'] = pd.DataFrame(format_data_lst)

        elif category == 'consume_utxo_mapping':
            formatted_all_data['consumed_utxo'] = pd.DataFrame(format_data_lst)

    # print("Formatted all data:", formatted_all_data)
    # If all fields are processed without errors
    return True, "Mapping validation passed.", formatted_all_data


def get_chain_id(lst, chain):
    for chain_data in lst:
        if chain_data['subchain'] == chain:
            return chain_data['id']


def load_metrics(script_path, meta_data, metrics, metric_chain_meta):
    """
    Load metric classes from a script and validate them using test data.

    :param script_path: Path to the Python script containing metric definitions.
    :return: A dictionary of metric class objects keyed by their 'chain' attribute.
    """
    # Load the script as a module
    module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    metric_meta = []
    metric_classes = {}
    for attribute_name in dir(module):

        attribute = getattr(module, attribute_name)

        if isinstance(attribute, type) and issubclass(attribute, CustomMetric) and attribute is not CustomMetric:
            # Instantiate the class
            metric_instance = attribute()

            if metric_instance.name == "" or metric_instance.name is None:
                raise Exception(f"Metric Name cannot be empty.")

            if metric_instance.name in metrics:
                raise Exception(f"Duplicate metric name: {metric_instance.name}")

            metric_meta.append({
                'id': metric_instance.name,
                'description': metric_instance.description,
                'category': metric_instance.category,
                'display_name': metric_instance.display_name,
                'type': 'custom',
                'grouping_type': None,
                'formula': None
            })

            chain = metric_instance.chain

            chain_id = get_chain_id(meta_data, chain)

            metric_chain_meta.append({
                'id': str(uuid.uuid4()),
                'blockchain_id': chain_id,
                'blockchain': metric_instance.blockchain,
                'sub_chain': metric_instance.chain,
                'metric_name': metric_instance.name
            })

            if chain not in metric_classes:
                metric_classes[chain] = [attribute]
            else:
                metric_classes[chain].append(attribute)

    return metric_classes, metric_meta, metric_chain_meta


def validate_custom_metrics(metric_classes, test_data):
    for chain, metric_classes in metric_classes.items():
        for metric_class in metric_classes:
            metric_obj = metric_class()
            chain_test_data = test_data[chain]
            type_ = metric_obj.transaction_type
            data = chain_test_data[type_]
            try:
                _ = metric_obj.calculate(data)
            except Exception as e:
                logger.log_error(e)
                return False

    return True


def validate_extract_and_mapper(extraction_path, mapper_path, start_date, pbar, config):
    final_validation = False

    test_input = start_date

    extract_validation_passed, extract_validation_message, extract_output, extract_func = validate_extraction_file(
        extraction_path, test_input)

    if not extract_validation_passed:
        # logger.log_error(extract_validation_message)
        return False, extract_validation_message, None, None, None, pbar

    pbar.update(20)

    mapper_validation_passed, mapper_validation_message, mappings, mapper_funcs = validate_mapper_file(mapper_path, config)

    if not mapper_validation_passed:
        # logger.log_error(mapper_validation_message)
        return False, mapper_validation_message, None, None, None, pbar

    pbar.update(20)

    if extract_validation_passed and mapper_validation_passed:
        final_validation, validation_message, formatted_test_data = validate_mapping_with_functions(mappings,
                                                                                                    extract_output,
                                                                                                    mapper_funcs)
        pbar.update(20)

    funcs = mapper_funcs
    funcs['extract'] = extract_func

    return final_validation, validation_message, funcs, mappings, formatted_test_data, pbar
