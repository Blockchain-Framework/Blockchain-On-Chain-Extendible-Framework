import re
import os
from ..logs import Logger

logger = Logger("GodSight")

def write_functions_to_new_scripts(func_data_list, output_dir):
    """
    Extracts specified functions from source files for each item in func_data_list and writes them to new script files.

    :param func_data_list: List of dictionaries containing 'id', 'funcs', and 'source_files'.
    :param output_dir: Directory where the output script files will be saved.
    """
    func_def_pattern_template = r'^def\s+({func_names})\s*\('

    for item in func_data_list:
        script_id = item['id']
        function_names = item['funcs']
        source_files = item['sources_files']
        
        func_def_pattern = re.compile(func_def_pattern_template.format(
            func_names='|'.join(function_names)
        ))

        extracted_functions = []

        for file_path in source_files:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            within_func = False
            func_lines = []
            
            for line in lines:
                if func_def_pattern.match(line):
                    within_func = True
                    func_lines = [line]
                elif within_func:
                    func_lines.append(line)
                    if line == '\n' or (line.strip() == '' and not line.startswith('    ')):
                        within_func = False
                        extracted_functions.extend(func_lines)
                        extracted_functions.append('\n')  # Space between functions

        # Construct the output file path using the script_id
        output_file_path = os.path.join(output_dir, f"{script_id}.py")

        # Write the extracted functions to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(extracted_functions)

        logger.log_info(f"Functions written to {output_file_path}")

