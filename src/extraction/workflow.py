import pandas as pd
import uuid
from utils.database.database_service import get_query_results, append_dataframe_to_sql, batch_insert_dataframes
from utils.scripts.utils.log_utils import log_workflow_status

from dotenv import load_dotenv

# Assuming the necessary imports are correctly set up
from utils.scripts.mappers import data_mapper
from utils.scripts.extraction_helper import store_data, dataframe_to_mapping_dict, extract_function_names, get_function, load_functions_from_file, get_transaction_mappings, get_emitted_utxo_mappings, get_consumed_utxo_mappings
from utils.scripts.mapper_helper import load_config_from_file, insert_feature_mapping_to_df

load_dotenv()


def store_configuration(blockchain, subchain, id):
    # Load configuration from file
    config_path = f'user_functions/mappers/{id}.py'
    config = load_config_from_file(config_path)
    
    # Insert mappings into the database
    trx_df = insert_feature_mapping_to_df(blockchain, subchain, config['trx_mapping'])
    emit_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['emit_utxo_mapping'])
    consume_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['consume_utxo_mapping'])
    
    trx_df._table_name = 'transactions_feature_mappings'
    emit_utxo_df._table_name  = 'emitted_utxos_feature_mappings'
    consume_utxo_df._table_name  = 'consumed_utxos_feature_mappings'
    
    batch_insert_dataframes([trx_df, emit_utxo_df, consume_utxo_df])


def extract_and_store_data(blockchain, subchain, date, id):
    # Extract feature mappings from the database
    transaction_mappings_df = get_transaction_mappings(blockchain, subchain)
    emitted_utxo_mappings_df = get_emitted_utxo_mappings(blockchain, subchain)
    consumed_utxo_mappings_df = get_consumed_utxo_mappings(blockchain, subchain)
    
    # Convert DataFrames to mapping dictionaries
    transaction_feature_mapping = dataframe_to_mapping_dict(transaction_mappings_df)
    emit_utxo_mapping = dataframe_to_mapping_dict(emitted_utxo_mappings_df)
    consume_utxo_mapping = dataframe_to_mapping_dict(consumed_utxo_mappings_df)
    
    # Extract function names and load functions
    all_function_names = list(set(extract_function_names(transaction_mappings_df) + 
                                  extract_function_names(emitted_utxo_mappings_df) + 
                                  extract_function_names(consumed_utxo_mappings_df)))
    
    functions_file_path = f'user_functions/functions/{id}.py'
    functions = load_functions_from_file(functions_file_path, all_function_names)
    
    # Prepare config for data mapper
    config = [
        transaction_feature_mapping,
        emit_utxo_mapping,
        consume_utxo_mapping,
        functions
    ]
    
    # Extract data using the extract function
    extract = get_function(functions_file_path, 'extract')
    trxs, emitted_utxos, consumed_utxos = extract(date)
    
    # Map and store data
    trxs, emitted_utxos, consumed_utxos = data_mapper(config, trxs, emitted_utxos, consumed_utxos)
    log_workflow_status(blockchain, subchain, 'start', 'extraction', None)
    try:
        store_data(sub_chain, date, trxs, emitted_utxos, consumed_utxos)
    except Exception as e:
        log_workflow_status(blockchain, subchain, 'fail', 'extraction', str(e))
    finally:
        log_workflow_status(blockchain, subchain, 'end', 'extraction', None)

def add_blockchain_configuration(blockchain, sub_chain, start_date):
    """Insert a new blockchain configuration into the blockchain_table."""        
    # Generate a unique ID
    unique_id = str(uuid.uuid4())
    
    # Prepare the INSERT statement
    df = pd.DataFrame({
        'id': [unique_id],
        'blockchain': [blockchain],
        'sub_chain':[sub_chain],
        'start_date':[start_date]
    })
    try:
        append_dataframe_to_sql('blockchain_table',df)
        return unique_id
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 
    
if __name__ == "__main__":
    blockchain = "Avalanche"
    sub_chain = "x"
    start_date = "2024-02-06"  # Example start date
    date_range = ["2024-02-07"] 
    
    # Optionally add blockchain configuration to blockchain_table
    # id = add_blockchain_configuration(blockchain, sub_chain, start_date)
    
    # Optionally store new configuration to the database (uncomment if needed)
    # store_configuration(blockchain, sub_chain, 'd3976d76-e9f4-49a2-b311-4d29b4bed400')

    # # Extract and store data for each day in the date range
    for day in date_range:
        extract_and_store_data(blockchain, sub_chain, day, 'd3976d76-e9f4-49a2-b311-4d29b4bed400')
