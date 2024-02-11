import re
import os
from ..logs import Logger

logger = Logger("GodSight")

hardcoded_imports = """from utils.scripts.utils.http_utils import fetch_transactions\nfrom utils.scripts.utils.time_utils import convert_to_gmt_timestamp\n\n"""


def write_functions_to_new_scripts(func_data_list, output_dir):
    # This pattern attempts to find function definitions more reliably and decorators
    func_def_pattern_template = r'(@[\w\.]+[\s]*)*^def\s+({func_names})\s*\(([\s\S]*?)\):'


    for item in func_data_list:
        script_id = item['id']
        function_names = item['funcs']
        source_files = item['sources_files']

        # Extended regex pattern to potentially match decorators as well
        func_def_pattern = re.compile(func_def_pattern_template.format(func_names='|'.join(function_names)), re.MULTILINE)

        extracted_functions = [hardcoded_imports]

        for file_path in source_files:
            with open(file_path, 'r') as file:
                content = file.read()

            matches = func_def_pattern.finditer(content)
            for match in matches:
                # Assuming function bodies are correctly indented following PEP 8
                start = match.start()
                end = match.end()
                indent_level = len(match.group(0)) - len(match.group(0).lstrip())
                # Find the end of the function body by looking for a decrease in indentation
                func_body_end = content.find('\n\n', end)
                extracted_functions.append(content[start:func_body_end])

        # Write the extracted functions to the output file
        output_file_path = os.path.join(output_dir, f"{script_id}.py")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(extracted_functions)

def is_import_statement(line):
    """Check if a line is an import statement."""
    return line.strip().startswith('import ') or line.strip().startswith('from ')

def combine_scripts_ignore_imports(source_file_paths, output_file_path):
    """
    Combines scripts into one, ignoring import statements and correcting indentation.

    :param source_file_paths: List of paths to the source script files.
    :param output_file_path: Path where the combined script will be saved.
    :param hardcoded_imports: String containing the hardcoded import statements to include.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w') as output_file:
        # Write hardcoded imports first
        output_file.write(hardcoded_imports + "\n\n")

        for file_path in source_file_paths:
            with open(file_path, 'r') as source_file:
                output_file.write(f"# Content from {os.path.basename(file_path)}\n")
                inside_function = False
                for line in source_file:
                    if is_import_statement(line):
                        # Skip import statements
                        continue
                    if line.startswith('def '):
                        inside_function = True
                        output_file.write("\n" + line)  # Ensure a newline before function definition
                    elif inside_function and (line.strip() == "" or not line.startswith('    ')):
                        # If we reach an empty line or a non-indented line after a function,
                        # it signifies the end of the function body
                        inside_function = False
                        output_file.write(line)
                    elif inside_function:
                        # Write lines inside functions with their indentation preserved
                        output_file.write(line)
                    elif not inside_function and line.strip():
                        # Write non-function lines that are not empty, adjusting indentation if necessary
                        output_file.write(line.lstrip())



