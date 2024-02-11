from datetime import datetime
from utils.model.model import model
import importlib.util
import os
import sys
from .blockchains.extract import extract_ava
from .blockchains.mappers import mapper_ava

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

def validate_extraction_function(file_name, relative_path_from_project_root, test_input):
    """
    Validate the extraction function in the specified file.

    :param file_name: Name of the Python file (without '.py') to be validated.
    :param relative_path_from_project_root: Relative path from the project root to the Python file.
    :param test_input: Test input to pass to the extract function.
    :return: Tuple (Boolean indicating whether the validation passed, and an error message if it failed).
    """
    # Construct the full file path
    # file_path = os.path.join(os.getcwd(), relative_path_from_project_root, file_name + '.py')
    # print(file_path)

    # # Ensure the file exists
    # if not os.path.isfile(file_path):
    #     return False, "File not found."

    # # Dynamically load the module using the provided utility function
    # module_name = "extract_module"
    # module = load_module_from_path(module_name, file_path)

    module = load_and_access_script(relative_path_from_project_root, file_name + '.py')

    # Validate the presence of the 'extract' function
    if not hasattr(module, 'extract'):
        return False, "The 'extract' function is not defined."

    # Test the 'extract' function with the provided input
    try:
        output = module.extract(test_input)
        # Validate the output's structure
        # Check if output is a tuple (or list) of exactly three elements
        if not isinstance(output, (list, tuple)) or len(output) != 3:
            return False, "Invalid output structure. Expected a tuple or list of three elements."
        
        # Validate each element in the output
        for element in output:
            if not isinstance(element, (list, tuple)) or not all(isinstance(item, dict) for item in element):
                return False, "Invalid output structure. Each element must be a list or tuple of dictionaries."
            
    except Exception as e:
        return False, f"Error executing the 'extract' function: {e}"

    return True, "Validation passed."


def validate_mapper_file(file_name, relative_path_from_project_root):

    # file_path = os.path.join(os.getcwd(), relative_path_from_project_root, file_name+'.py')

    mapper_funcs = []

    # if not os.path.exists(file_path):
    #     return False, "Mapper file does not exist."

    # module_name = os.path.basename(file_path).replace('.py', '')
    # spec = importlib.util.spec_from_file_location(module_name, file_path)
    # mapper_module = importlib.util.module_from_spec(spec)

    mapper_module = mapper_ava

    # try:
    #     spec.loader.exec_module(mapper_module)
    # except Exception as e:
    #     return False, f"Failed to load the mapper module from {file_path}: {e}"

    if not hasattr(mapper_module, 'config'):
        return False, "No 'config' found in the mapper module."
    
    if not isinstance(model, dict):
        raise TypeError("model is expected to be a dictionary.")

    # Validate the config structure against the model
    for category, mappings in model.items():
        if category not in mapper_module.config:
            return False, f"Missing '{category}' in mapper config.", None, []

        for field, _ in mappings.items():
            if field not in mapper_module.config[category]:
                return False, f"Missing '{field}' in '{category}'.", None, []

            config_field = mapper_module.config[category].get(field)
            if not config_field:
                return False, f"Configuration for '{field}' in '{category}' is not defined.", None, []
            
            if len(config_field)<2:
                return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []
            
            if config_field[1] == "function":
                if len(config_field)<3:
                    return False, f"Configuration for '{field}' in '{category}' is not correct.", None, []
                
                if config_field[1] != "function" or not hasattr(mapper_module, config_field[2]):
                    return False, f"The function '{config_field[2]}' for '{field}' in '{category}' does not exist.", None, []
                
                mapper_funcs.append(config_field[2])

    return True, "Mapper validation passed.", mapper_module.config, mapper_funcs



def validate_extract_and_mapper(extraction_file_name, mapper_file_name, extraction_path, mapper_path, start_date):
    test_input = start_date
    
    extract_validation_passed, extract_validation_message = validate_extraction_function(extraction_file_name, extraction_path, test_input)
    
    mapper_validation_passed, mapper_validation_message, mappings, mapper_funcs = validate_mapper_file(mapper_file_name, mapper_path)
    
    funcs = ['extract'] + mapper_funcs

    return extract_validation_passed, mapper_validation_passed, extract_validation_message, mapper_validation_message, mappings, funcs


