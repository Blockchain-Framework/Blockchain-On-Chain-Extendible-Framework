import re
import os
import inspect
import ast
import astor  # If using Python version < 3.9
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
        for function_dict in functions_list:

            output_file = os.path.join(output_file_path, str(function_dict['id']) + '.py')

            with open(output_file, 'w') as file:
                # Write import statements
                for import_statement in imports:
                    file.write(import_statement + '\n')
                if imports:
                    file.write('\n')  # Add an extra newline for separation

                # Write function source code for each entry in the functions list
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
            for chain, classes in metric_classes.items():
                for metric_class in classes:
                    try:
                        # Retrieve the source code of the current class
                        source_code = inspect.getsource(metric_class)
                        # Write the source code to the output file
                        output_file.write(source_code)
                        # Add two newlines for spacing between class definitions
                        output_file.write('\n\n')
                    except Exception as e:
                        print(e)
                        print(f"Error retrieving source for {metric_class}: {e}")
                        return False

        return True
    except Exception as e:
        print(f"Error writing metric classes to file: {e}")
        return False


def extract_and_write_class_definitions(user_script_path, framework_script_path, additional_imports=[]):
    # Read the user's script
    with open(user_script_path, 'r') as file:
        user_script_source = file.read()

    # Parse the source code into an AST
    parsed_ast = ast.parse(user_script_source)

    # Filter for class definitions
    class_definitions = [node for node in parsed_ast.body if isinstance(node, ast.ClassDef)]

    # Serialize class definitions back into source code
    class_sources = [astor.to_source(class_def) for class_def in
                     class_definitions]  # Use ast.unparse(class_def) for Python 3.9+

    # Determine the file mode (append if file exists, write otherwise)
    file_mode = 'a' if os.path.exists(framework_script_path) else 'w'

    # Write or append to the framework's script file
    with open(framework_script_path, file_mode) as file:
        # If appending, add a newline for separation from existing content
        if file_mode == 'a':
            file.write('\n\n')  # Ensure separation from existing content

        # Optionally write additional imports when creating a new file
        if additional_imports and file_mode == 'w':
            for import_statement in additional_imports:
                file.write(import_statement + '\n')
            file.write('\n')  # Add an extra newline for separation

        # Write class source code
        for source_code in class_sources:
            file.write(source_code + '\n\n')

    return True
