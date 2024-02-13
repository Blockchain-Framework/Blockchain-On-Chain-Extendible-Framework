import shutil
import os

import pandas as pd


def format_config_for_insertion(config, blockchain_name, subchain_name):
    table_names = {
        'trx_mapping': 'transactions_feature_mappings',
        'emit_utxo_mapping': 'emitted_utxos_feature_mappings',
        'consume_utxo_mapping': 'consumed_utxos_feature_mappings'
    }
    formatted_data = {
        'transactions_feature_mappings': [],
        'emitted_utxos_feature_mappings': [],
        'consumed_utxos_feature_mappings': []
    }

    for mapping_type, mappings in config.items():
        table_name = table_names[f"{mapping_type}"]  # Map config keys to table names
        for source_field, mapping_info in mappings.items():
            target_field, type_, info = mapping_info[0], mapping_info[1], None
            if len(mapping_info) > 2:
                info = mapping_info[2]  # Function name if it's a function mapping

            formatted_entry = {
                'blockchain': blockchain_name,
                'subchain': subchain_name,
                'sourceField': source_field,
                'targetField': target_field,
                'type': type_,
                'info': info
            }
            formatted_data[table_name].append(formatted_entry)

    return formatted_data


def copy_file(source_path, destination_path):
    """
    Copies a file from the source path to the destination path.

    Parameters:
    - source_path: The path of the source file.
    - destination_path: The path where the file should be copied.
    """
    try:
        shutil.copy(source_path, destination_path)
        # print("File copied successfully!")
    except Exception as e:
        # print(f"Error copying file: {e}")
        raise Exception(e)


def delete_file(file_path):
    """
    Deletes a file at the given path.

    Parameters:
    - file_path: The path of the file to delete.
    """
    try:
        os.remove(file_path)
        # print("File deleted successfully!")
    except Exception as e:
        # print(f"Error deleting file: {e}")
        raise Exception(e)


def delete_files_in_directory(directory_path):
    """
    Deletes all files within the specified directory.

    Parameters:
    - directory_path: The path of the directory from which all files will be deleted.
    """
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                # print(f"Deleted {file_path}")
            else:
                print(f"Skipping {file_path}, not a file or link")
        # print("All files deleted successfully!")
    except Exception as e:
        # print(f"Error deleting files: {e}")
        raise Exception(e)


def concatenate_and_fill_dfs(all_test_data):
    """
    Concatenates DataFrames from a nested dictionary structure, fills missing values with 0,
    and organizes them by transaction type.

    :param all_test_data: A nested dictionary with structure {chain: {type_: DataFrame}}
    :return: A dictionary with keys as transaction types and values as concatenated DataFrames.
    """
    test_data = {}
    type_dfs = {}

    # Aggregate DataFrames by transaction type
    for chain_data in all_test_data.values():
        for type_, df in chain_data.items():
            type_dfs.setdefault(type_, []).append(df)

    # Concatenate and fill missing values for each transaction type
    for type_, dfs in type_dfs.items():
        concatenated_df = pd.concat(dfs, ignore_index=True, sort=False).fillna(0)
        test_data[type_] = concatenated_df

    return test_data
