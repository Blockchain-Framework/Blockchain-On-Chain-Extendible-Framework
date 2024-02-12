from datetime import datetime
from utils.model.model import model
import importlib.util
import os
import sys
from .blockchains.extract import extract_ava
from .blockchains.mappers import mapper_ava

from ..logs import Logger

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
    #TODO: check this below line - ERROR:  attempted relative import beyond top-level package
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

from pathlib import Path

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


def load_and_access_script(relative_path, script_name):
    """
    Load a Python script dynamically at runtime and access its functions and variables.
    
    Args:
        relative_path (str): The relative path to the directory containing the script.
        script_name (str): The name of the script to load.
        
    Returns:
        module: The loaded module.
    """
    # Construct the absolute path to the scrip
    # abs_path = r'E:\Academic Works\7 Sem Academic\FYP\Blockchain-On-Chain-Extendible-Framework\src\utils\handler\blockchains\extract\d3976d76-e9f4-49a2-b311-4d29b4bed400.py'


    # # Check if the script is already loaded
    # if script_name in sys.modules:
    #     module = sys.modules[script_name]
    # else:
    #     # Load the module dynamically
    #     spec = importlib.util.spec_from_file_location(script_name, abs_path)
    #     module = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(module)

    return extract_ava

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

    print('done')

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
        return False, "The 'mapper' file is not exist.",  None, []
    
    if not is_python_file(relative_path_from_project_root):
        return False, "The 'mapper' file is not a python script.",  None, []
    
    mapper_config = load_config_from_file(relative_path_from_project_root)

    if mapper_config is None:
        return False, "No 'config' found in the mapper module.",  None, []
    
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
            
            if len(config_field)<2:
                return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []
            
            if config_field[1] == "function":
                if len(config_field)<3:
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
    for category, mappings in mapper_config.items():
        test_data = None

        if category=='':
            data = extracted_data[0]
            if data:
                test_data = data[0]

        elif category=='':
            data = extracted_data[0]
            if data:
                test_data = data[0]

        elif category=='':
            data = extracted_data[0]
            if data:
                test_data = data[0]
        
        else:
            return False, f"Invalid category in mapper config"

        for field, mapping_details in mappings.items():
            if field not in test_data:
                return False, f"Field '{field}' not present in sample data."

            mapping_type = mapping_details[1]
            if mapping_type == "function":
                function_name = mapping_details[2]
                if function_name not in functions:
                    return False, f"Function '{function_name}' required for mapping '{field}' is not loaded."

                # Attempt to apply the function to the field value from the sample data
                try:
                    # Here, we assume the functions take the field value and return a processed value
                    _ = functions[function_name](test_data[field])
                except Exception as e:
                    return False, f"Error applying function '{function_name}' to field '{field}': {e}"


    # If all fields are processed without errors
    return True, "Mapping validation passed."



def validate_extract_and_mapper(extraction_path, mapper_path, start_date):

    final_validation = False

    test_input = start_date
    
    extract_validation_passed, extract_validation_message, extract_output, extract_func = validate_extraction_file( extraction_path, test_input)
    print(extract_validation_message)
    
    mapper_validation_passed, mapper_validation_message, mappings, mapper_funcs = validate_mapper_file(mapper_path)
    print(mapper_validation_message)

    if not extract_validation_passed:
        # logger.log_error(extract_validation_message)
        return False, extract_validation_message, None, None
    
    if not mapper_validation_passed:
        # logger.log_error(mapper_validation_message)
        return False, mapper_validation_message, None, None

    if extract_validation_passed and mapper_validation_passed:
        final_validation, validation_message = validate_mapping_with_functions(mappings, extract_output, mapper_funcs)
    
    funcs = mapper_funcs
    funcs['extract'] = extract_func

    return final_validation, validation_message, funcs, mappings


