import re
import os
import inspect
from ..logs.log import Logger

logger = Logger("GodSight")


def write_functions_to_file(functions_list, output_file_path, imports=[]):
    """
    Writes the specified imports and source code of given functions from a list of dictionaries
    each containing function objects, to a new script file.

    Parameters:
    - functions_list (list): A list of dictionaries with 'id', 'funcs' (function objects), and 'source_files'.
    - output_file_path (str): Path to the output script file.
    - imports (list): A list of import statements as strings to be included at the top of the file.

    Returns:
    - bool: True if successful, False otherwise.
    """
    try:
        with open(output_file_path, 'w') as file:
            # Write import statements
            for import_statement in imports:
                file.write(import_statement + '\n')
            if imports:
                file.write('\n')  # Add an extra newline for separation

            # Write function source code for each entry in the functions list
            for function_dict in functions_list:
                for func_name, func in function_dict['funcs'].items():
                    source = inspect.getsource(func)
                    file.write(source + '\n\n')
        return True
    except Exception as e:
        print(f"Error writing functions to file: {e}")
        return False


def write_metric_classes_to_script(metric_classes, output_script_path, imports=[]):
    """
    Writes or appends metric class definitions to a specified script file.

    :param metric_classes: A list of metric class types to be written.
    :param output_script_path: The path to the output script file where the classes will be written or appended.
    """
    # Determine the mode to open the file ('a' for append if file exists, 'w' otherwise)
    try:
        file_mode = 'a' if os.path.exists(output_script_path) else 'w'

        with open(output_script_path, file_mode) as output_file:
            # If appending, add a newline for separation from existing content
            if file_mode == 'w':
                for import_statement in imports:
                    output_file.write(import_statement + '\n')
                if imports:
                    output_file.write('\n')

            elif file_mode == 'a':
                output_file.write('\n\n')

            # Iterate over each class to write its source code to the file
            for metric_class in metric_classes:
                # Get the source code of the class
                source_code = inspect.getsource(metric_class)
                # Write the source code to the output file
                output_file.write(source_code)
                # Add two newlines for spacing between classes
                output_file.write('\n\n')

        return True
    except Exception as e:
        print(f"Error writing metric classes to file: {e}")
        return False

