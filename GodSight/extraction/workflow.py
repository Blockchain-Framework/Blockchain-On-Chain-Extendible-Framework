from GodSight.extraction.utils.scripts.utils.log_utils import log_workflow_status
from .logs.log import Logger
import os

logger = Logger("GodSight")

# Assuming the necessary imports are correctly set up
from GodSight.extraction.utils.scripts.mappers import data_mapper
from GodSight.extraction.utils.scripts.extraction_helper import store_data, dataframe_to_mapping_dict, extract_function_names, get_function, load_functions_from_file, get_transaction_mappings, get_emitted_utxo_mappings, get_consumed_utxo_mappings
from GodSight.extraction.utils.scripts.mapper_helper import load_config_from_file, insert_feature_mapping_to_df



# def store_configuration(blockchain, subchain, id):
#     # Load configuration from file
#     config_path = f'user_functions/mappers/{id}.py'
#     config = load_config_from_file(config_path)
    
#     # Insert mappings into the database
#     trx_df = insert_feature_mapping_to_df(blockchain, subchain, config['trx_mapping'])
#     emit_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['emit_utxo_mapping'])
#     consume_utxo_df = insert_feature_mapping_to_df(blockchain, subchain, config['consume_utxo_mapping'])
    
#     trx_df._table_name = 'transactions_feature_mappings'
#     emit_utxo_df._table_name  = 'emitted_utxos_feature_mappings'
#     consume_utxo_df._table_name  = 'consumed_utxos_feature_mappings'
    
#     batch_insert_dataframes([trx_df, emit_utxo_df, consume_utxo_df])


def extract_and_store_data(blockchain, subchain, date, id, config):
    logger.log_info(f"Transaction extraction strats for {blockchain} {subchain} date:{date}")

    # Extract feature mappings from the database
    transaction_mappings_df = get_transaction_mappings(blockchain, subchain, config)
    emitted_utxo_mappings_df = get_emitted_utxo_mappings(blockchain, subchain, config)
    consumed_utxo_mappings_df = get_consumed_utxo_mappings(blockchain, subchain, config)
    
    # Convert DataFrames to mapping dictionaries
    transaction_feature_mapping = dataframe_to_mapping_dict(transaction_mappings_df)
    emit_utxo_mapping = dataframe_to_mapping_dict(emitted_utxo_mappings_df)
    consume_utxo_mapping = dataframe_to_mapping_dict(consumed_utxo_mappings_df)
    
    # Extract function names and load functions
    all_function_names = list(set(extract_function_names(transaction_mappings_df) + 
                                  extract_function_names(emitted_utxo_mappings_df) + 
                                  extract_function_names(consumed_utxo_mappings_df)))
    
    # functions_file_path = f'user_functions/{id}.py'
    functions_file_path = os.path.join('GodSight/extraction/user_functions', str(id) + '.py')
    functions = load_functions_from_file(functions_file_path, all_function_names)
    
    # Prepare config for data mapper
    config_ = [
        transaction_feature_mapping,
        emit_utxo_mapping,
        consume_utxo_mapping,
        functions
    ]
    
    # Extract data using the extract function
    extract = get_function(functions_file_path, 'extract')
    trxs, emitted_utxos, consumed_utxos = extract(date)
    
    logger.log_info(f"Transaction extraction finished for {blockchain} {subchain}  date:{date}")
    
    # Map and store data
    trxs, emitted_utxos, consumed_utxos = data_mapper(config_, trxs, emitted_utxos, consumed_utxos)

    log_workflow_status(blockchain, subchain, 'start', 'extraction', None, config)
    try:
        logger.log_info(f"Started storing transactions for {blockchain} {subchain} on date: {date}")
        store_data(subchain, date, trxs, emitted_utxos, consumed_utxos, config)
        logger.log_info(f"Finished storing transactions for {blockchain} {subchain} on date: {date}")
    except Exception as e:
        logger.log_error(f"An unexpected error occurred while storing transactions: {e}")
        log_workflow_status(blockchain, subchain, 'fail', 'extraction', str(e), config)
    finally:
        log_workflow_status(blockchain, subchain, 'end', 'extraction', None, config)


if __name__ == "__main__":
    blockchain = "Avalanche"
    sub_chain = "x"
    start_date = "2024-02-06"  # Example start date
    date_range = ["2024-02-14"] 

    for day in date_range:
        extract_and_store_data(blockchain, sub_chain, day, '7dd13be3-c489-48eb-8826-7ad9119ba65a')
