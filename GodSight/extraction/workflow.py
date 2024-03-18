from extraction.utils.database.database_service import store_all_extracted_data
from extraction.utils.database.services import check_subchain_last_extracted_date, get_subchain_start_date
from extraction.utils.scripts.utils.log_utils import log_workflow_status

import os
from datetime import datetime, timedelta

from .logs.log import Logger
logger = Logger("GodSight")

# Assuming the necessary imports are correctly set up
from extraction.utils.scripts.mappers import data_mapper, transform_data
from extraction.utils.scripts.extraction_helper import store_data, dataframe_to_mapping_dict, \
    extract_function_names, get_function, load_functions_from_file, get_transaction_mappings, get_emitted_utxo_mappings, \
    get_consumed_utxo_mappings
from extraction.utils.scripts.mapper_helper import load_config_from_file, insert_feature_mapping_to_df


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


def extract_and_store_data(blockchain, subchain, end_date, id, config):
    last_extracted_date = check_subchain_last_extracted_date(config, blockchain, subchain)

    if last_extracted_date is None:
        start_date = get_subchain_start_date(config, blockchain, subchain)
    else:
        start_date = last_extracted_date

    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    if end_date < start_date:
        return

    current_loop_date = start_date
    while current_loop_date <= end_date:

        date = current_loop_date.strftime("%Y-%m-%d")

        try:

            logger.log_info(f"Transaction extraction starts for {blockchain} {subchain} date:{date}")

            log_workflow_status(blockchain, subchain, 'start', 'extraction', None, config)

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
            functions_file_path = os.path.join('/user_functions', str(id) + '.py')
            functions = load_functions_from_file(functions_file_path, all_function_names)

            # Extract data using the extract function
            extract = get_function(functions_file_path, 'extract')
            trxs, emitted_utxos, consumed_utxos = extract(date)

            logger.log_info(f"Transaction extraction finished for {blockchain} {subchain}  date:{date}")

            # Map and store data
            # trxs, emitted_utxos, consumed_utxos = data_mapper(config_, trxs, emitted_utxos, consumed_utxos, config)

            transformed_trxs, transformed_emitted_utxos, transformed_consumed_utxos= transform_data(blockchain, subchain, trxs, emitted_utxos, consumed_utxos, functions, config)


            logger.log_info(f"Started storing transactions for {blockchain} {subchain} on date: {date}")
            # store_data(subchain, date, trxs, emitted_utxos, consumed_utxos, config)
            store_all_extracted_data(blockchain, subchain, date, transformed_trxs, transformed_emitted_utxos,
                                     transformed_consumed_utxos, config)
            logger.log_info(f"Finished storing transactions for {blockchain} {subchain} on date: {date}")

            log_workflow_status(blockchain, subchain, 'success', 'extraction', None, config)

        except Exception as e:
            logger.log_error(f"An unexpected error occurred while storing transactions: {e}")
            log_workflow_status(blockchain, subchain, 'fail', 'extraction', str(e), config)
            # TODO: Delete all the data for this date before leaving
            raise Exception(e)

        current_loop_date += timedelta(days=1)


if __name__ == "__main__":
    blockchain = "Avalanche"
    sub_chain = "x"
    start_date = "2024-02-06"  # Example start date
    date_range = ["2024-02-14"]

    for day in date_range:
        extract_and_store_data(blockchain, sub_chain, day, '7dd13be3-c489-48eb-8826-7ad9119ba65a')
