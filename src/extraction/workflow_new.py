import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy import text
import importlib.util
import pandas as pd
from utils.database.database_service import get_query_results, append_dataframe_to_sql, batch_insert_dataframes
# from utils.scripts.utils import log_workflow_status

from dotenv import load_dotenv

# Assuming the necessary imports are correctly set up
from utils.scripts.extraction import extract_avalanche_data
from utils.scripts.mappers import data_mapper
from utils.scripts.helper import store_data

load_dotenv()

class DataExtractionWorkflowManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")
        self.engine = create_engine(self.db_connection_string)

    def get_transaction_mappings(self, blockchain, subchain):
        query = text(f"""
        SELECT * FROM transactions_feature_mappings
        WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
        """)
        return get_query_results(query, self.db_connection_string)

    def get_emitted_utxo_mappings(self, blockchain, subchain):
        query = text(f"""
        SELECT * FROM emitted_utxos_feature_mappings
        WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
        """)
        return get_query_results(query, self.db_connection_string)
    
    def get_consumed_utxo_mappings(self, blockchain, subchain):
        query = text(f"""
        SELECT * FROM consumed_utxos_feature_mappings
        WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
        """)
        return get_query_results(query, self.db_connection_string)

    def convert_df_to_config(self, df):
        feature_mapping = {}
        transformation_functions = {}

        for _, row in df.iterrows():
            source_field = row['sourcefield']
            target_field = row['targetfield']
            mapping_type = row['type']
            function_info = row['info']

            if mapping_type == 'feature':
                # For 'feature' type, directly map the source field to the target field
                feature_mapping[target_field] = (source_field, "feature")
            elif mapping_type == 'function':
                # For 'function' type, store the function mapping
                feature_mapping[target_field] = (source_field, "function", function_info)
                # Assuming you have a dictionary or a way to relate function_info strings to actual function objects
                if function_info in globals():
                    transformation_functions[function_info] = globals()[function_info]

        return feature_mapping, transformation_functions

    # The 'feature_mapping' and 'transformation_functions' can now be used in your workflow
    def run_workflow(self, start_date, end_date, blockchain, subchain):
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        while current_date <= end_date:
            self.logger.info(f"Processing date: {current_date.strftime('%Y-%m-%d')}")

            # Fetch configuration details from separate tables
            transaction_config = self.get_transaction_mappings(blockchain, subchain)
            emitted_utxo_config = self.get_emitted_utxo_mappings(blockchain, subchain)
            consumed_utxo_config = self.get_consumed_utxo_mappings(blockchain, subchain)

            # Combine configurations into a single config object if necessary
            config = {
                "transaction": transaction_config,
                "emitted_utxo": emitted_utxo_config,
                "consumed_utxo": consumed_utxo_config,
            }

            # Perform data extraction
            day_str = current_date.strftime("%Y-%m-%d")
            trxs, emitted_utxos, consumed_utxos = extract_avalanche_data(day_str)  # Adjust parameters as needed

            # Map and store data
            mapped_trxs, mapped_emitted_utxos, mapped_consumed_utxos = data_mapper(config, trxs, emitted_utxos, consumed_utxos)
            store_data(blockchain, day_str, mapped_trxs, mapped_emitted_utxos, mapped_consumed_utxos)

            current_date += timedelta(days=1)


def load_config_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module.config

def insert_feature_mapping_to_df(blockchain, subchain, mapping):
    # Convert the mapping dictionary to a DataFrame
    data = []
    for source_field, mapping_details in mapping.items():
        target_field, type = mapping_details[:2]
        info = mapping_details[2] if len(mapping_details) > 2 else None  # Get the function name if exists
        data.append({
            'blockchain': blockchain,
            'subchain': subchain,
            'source_field': source_field,
            'target_field': target_field,
            'type': type,
            'info': info or None  # Ensure None is used if info is not provided
        })
    
    df = pd.DataFrame(data)
    return df

def get_function(file_path, function_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    function_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(function_module)
    return getattr(function_module, function_name, None)  # Returns None if the function does not exist

def dataframe_to_mapping_dict(df):
    mapping_dict = {}
    for _, row in df.iterrows():
        if row['type'] == 'feature':
            mapping_dict[row['source_field']] = (row['target_field'], 'feature')
        elif row['type'] == 'function':
            mapping_dict[row['source_field']] = (row['target_field'], 'function', row['info'])
    return mapping_dict

def extract_function_names(df):
    # Filter the DataFrame to include only rows where the type is 'function'
    functions_df = df[df['type'] == 'function']
    # Extract the 'info' column which contains the function names
    function_names = functions_df['info'].tolist()
    return function_names

def load_functions_from_file(file_path, function_names):
    functions = {}
    for name in function_names:
        func = get_function(file_path, name)
        if func:
            functions[name] = func
    return functions

if __name__ == "__main__":
    blockchain = 'Avalanche'
    subchain = 'x'
    
    manager = DataExtractionWorkflowManager()
    
    """ Example of loading configuration from a file and using it to insert feature mappings into the database """
    # config = load_config_from_file(r'user_functions\avalanche_x\mappers.py')
    # print(config)
    
    # trx_df = insert_feature_mapping_to_df(blockchain, subchain, config['trx_mapping'])
    # trx_df._table_name = 'transactions_feature_mappings'

    # emit_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['emit_utxo_mapping'])
    # emit_utxo_df._table_name  = 'emitted_utxos_feature_mappings'

    # consume_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['consume_utxo_mapping'])
    # consume_utxo_df._table_name  = 'consumed_utxos_feature_mappings'

    # batch_insert_dataframes([trx_df, emit_utxo_df, consume_utxo_df])
    
    """ Example of extracting feature mappings from the database and using them to perform data extraction """
    
    transaction_mappings_df = manager.get_transaction_mappings(blockchain, subchain)
    emitted_utxo_mappings_df = manager.get_emitted_utxo_mappings(blockchain, subchain)
    consumed_utxo_mappings_df = manager.get_consumed_utxo_mappings(blockchain, subchain)
    
    print(transaction_mappings_df)
    print(emitted_utxo_mappings_df)
    print(consumed_utxo_mappings_df)
    
    print(transaction_mappings_df.columns)
    print(emitted_utxo_mappings_df.columns)
    print(consumed_utxo_mappings_df.columns)

    transaction_feature_mapping = dataframe_to_mapping_dict(transaction_mappings_df)
    emit_utxo_mapping = dataframe_to_mapping_dict(emitted_utxo_mappings_df)
    consume_utxo_mapping = dataframe_to_mapping_dict(consumed_utxo_mappings_df)

    print(transaction_feature_mapping)
    print(emit_utxo_mapping)
    print(consume_utxo_mapping)
    
    # Extract function names from each DataFrame
    transaction_function_names = extract_function_names(transaction_mappings_df)
    emitted_utxo_function_names = extract_function_names(emitted_utxo_mappings_df)
    consumed_utxo_function_names = extract_function_names(consumed_utxo_mappings_df)

    # Combine all function names into a single list and remove duplicates
    all_function_names = list(set(transaction_function_names + emitted_utxo_function_names + consumed_utxo_function_names))

    print(all_function_names)

    functions = load_functions_from_file(r'user_functions\avalanche_x\functions.py', all_function_names)
    
    print(functions)
    
    config = [
        transaction_feature_mapping,
        emit_utxo_mapping,
        consume_utxo_mapping,
        functions
    ]
    
    """extract functions"""
    day = "2024-02-06"
    extract = get_function(r'user_functions\avalanche_x\functions.py', 'extract')
    
    trxs, emitted_utxos, consumed_utxos  = extract(day)
    trxs, emitted_utxos, consumed_utxos = data_mapper(config, trxs, emitted_utxos, consumed_utxos)
    store_data('x', day, trxs, emitted_utxos, consumed_utxos)
    
    