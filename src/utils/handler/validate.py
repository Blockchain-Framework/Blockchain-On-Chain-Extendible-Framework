from datetime import datetime
from ..model import model
import importlib.util
import os

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


def validate_extraction_function(file_name, path, test_input):
    """
    Validate the extraction function in the specified file.

    :param file_path: Path to the extraction.py file to be validated.
    :param test_input: Test input to pass to the extract function.
    :return: Boolean indicating whether the validation passed, and an error message if it failed.
    """

    file_path = path + file_name

    # Ensure the file exists
    if not os.path.isfile(file_path):
        return False, "File not found."

    # Attempt to dynamically import the specified Python file
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return False, f"Failed to import module: {e}"

    # Check if the extract function exists
    if not hasattr(module, 'extract'):
        return False, "The 'extract' function is not defined."

    # Attempt to call the extract function with the test input
    try:
        output = module.extract(test_input)

        # Validate the output structure
        if not isinstance(output, (list, tuple)) or not all(isinstance(item, dict) for item in output):
            return False, "Invalid output structure. Expected a list or tuple of dictionaries."

    except Exception as e:
        return False, f"Error executing the 'extract' function: {e}"

    return True, "Validation passed."


def validate_mapper_file(file_name, path):

    file_path = path + file_name

    mapper_funcs = []

    if not os.path.exists(file_path):
        return False, "Mapper file does not exist."

    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mapper_module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(mapper_module)
    except Exception as e:
        return False, f"Failed to load the mapper module from {file_path}: {e}"

    if not hasattr(mapper_module, 'config'):
        return False, "No 'config' found in the mapper module."

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
    mapper_validation_passed, mapper_validation_message, mappings, mapper_funcs = validate_mapper_file(mapper_file_name, extraction_path)

    funcs = ['extract'] + mapper_funcs

    return extract_validation_passed, mapper_validation_passed, extract_validation_message, mapper_validation_message, mappings, funcs


