from datetime import datetime
from pathlib import Path
import importlib.util
import os
import sys
import pandas as pd
from src.utils.model.model import model
from src.utils.model.metric import BaseMetric, CustomMetric
from src.utils.handler.http import fetch_transactions
from src.utils.handler.time import convert_to_gmt_timestamp

from ..logs.log import Logger

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


def validate_mapper_file(relative_path_from_project_root):
    # file_path = os.path.join(os.getcwd(), relative_path_from_project_root, file_name+'.py')

    mapper_funcs_str = []

    if not file_exists(relative_path_from_project_root):
        return False, "The 'mapper' file is not exist.", None, []

    if not is_python_file(relative_path_from_project_root):
        return False, "The 'mapper' file is not a python script.", None, []

    mapper_config = load_config_from_file(relative_path_from_project_root)

    if mapper_config is None:
        return False, "No 'config' found in the mapper module.", None, []

    if not isinstance(model, dict):
        raise TypeError("model is expected to be a dictionary.")

    # Validate the config structure against the model
    for category, mappings in model.items():
        if category not in mapper_config:
            return False, f"Missing '{category}' in mapper config.", None, []

        for field, _ in mappings.items():
            if field not in mapper_config[category]:
                return False, f"Missing '{field}' in '{category}'.", None, []

            config_field = mapper_config[category].get(field)
            if not config_field:
                return False, f"Configuration for '{field}' in '{category}' is not defined.", None, []

            if len(config_field) < 2:
                return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []

            if config_field[1] == "function":
                if len(config_field) < 3:
                    return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []

                mapper_funcs_str.append(config_field[2])

    mapper_funcs, msg = load_functions_from_file(relative_path_from_project_root, mapper_funcs_str)

    if mapper_funcs is None:
        return False, f"'{msg}' is not a function in mapper file.", None, []

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

    formatted_all_data = {
    }

    for category, mappings in mapper_config.items():

        if category == 'trx_mapping':
            data = extracted_data[0]
            if data:
                test_data = data[:3]
            else:
                continue

        elif category == 'emit_utxo_mapping':
            data = extracted_data[1]
            if data:
                test_data = data[:3]
            else:
                continue

        elif category == 'consume_utxo_mapping':
            data = extracted_data[2]
            if data:
                test_data = data[:3]
            else:
                continue

        else:
            return False, f"Invalid category in mapper config"

        format_data_lst = []
        for test in test_data:
            format_data = {}
            for field, mapping_details in mappings.items():
                # TODO: if field is an function then field is not exist is okay
                mapping_field = mapping_details[0]
                mapping_type = mapping_details[1]
                if (mapping_field not in test) and mapping_type == "feature":
                    return False, f"Field '{field}' not present in sample data."

                if mapping_type == "feature":
                    format_data[field] = test[mapping_field]

                elif mapping_type == "function":
                    function_name = mapping_details[2]
                    if function_name not in functions:
                        return False, f"Function '{function_name}' required for mapping '{field}' is not loaded."

                    # Attempt to apply the function to the field value from the sample data
                    try:
                        # Here, we assume the functions take the field value and return a processed value
                        result = functions[function_name](test)

                        format_data[field] = result

                    except Exception as e:
                        return False, f"Error applying function '{function_name}' to field '{field}': {e}"

            format_data_lst.append(format_data)

        if category == 'trx_mapping':
            formatted_all_data['transaction'] = pd.DataFrame(format_data_lst)

        elif category == 'emit_utxo_mapping':
            formatted_all_data['emitted'] = pd.DataFrame(format_data_lst)

        elif category == 'consume_utxo_mapping':
            formatted_all_data['consumed'] = pd.DataFrame(format_data_lst)

    # If all fields are processed without errors
    return True, "Mapping validation passed.", formatted_all_data


def get_chain_id(lst, chain):
    for chain_data in lst:
        if chain_data['subchain'] == chain:
            return chain_data['id']


def load_metrics(script_path, meta_data, metrics):
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
    metric_chain_meta = []

    for chain_data in meta_data:
        for basic_metric in metrics:
            metric_chain_meta.append({
                'blockchain_id': chain_data['id'],
                'blockchain': chain_data['blockchain'],
                'sub_chain': chain_data['subchain'],
                'metric_name': basic_metric
            })

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
                'metric_name': metric_instance.name,
                'description': metric_instance.description,
                'category': metric_instance.category,
                'type': 'custom'
            })

            chain = metric_instance.chain

            chain_id = get_chain_id(meta_data, chain)

            metric_chain_meta.append({
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
                print(e)
                return False

    return True


def validate_extract_and_mapper(extraction_path, mapper_path, start_date):
    final_validation = False

    test_input = start_date

    extract_validation_passed, extract_validation_message, extract_output, extract_func = validate_extraction_file(
        extraction_path, test_input)

    mapper_validation_passed, mapper_validation_message, mappings, mapper_funcs = validate_mapper_file(mapper_path)

    if not extract_validation_passed:
        # logger.log_error(extract_validation_message)
        return False, extract_validation_message, None, None, None

    if not mapper_validation_passed:
        # logger.log_error(mapper_validation_message)
        return False, mapper_validation_message, None, None, None

    if extract_validation_passed and mapper_validation_passed:
        final_validation, validation_message, formatted_test_data = validate_mapping_with_functions(mappings,
                                                                                                    extract_output,
                                                                                                    mapper_funcs)

    funcs = mapper_funcs
    funcs['extract'] = extract_func

    return final_validation, validation_message, funcs, mappings, formatted_test_data
