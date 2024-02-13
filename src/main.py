import argparse
import sys
import os
import uuid
from config import Config
from utils.database.db import test_connection, initialize_database
from utils.database.services import check_blockchain_exists, insert_blockchain_metadata_and_mappings, \
    delete_blockchain_data

from utils.handler.fileReader import read_blockchain_metadata
from utils.handler.filerWriter import write_functions_to_file, write_metric_classes_to_script
from utils.handler.helper import format_config_for_insertion, copy_file, delete_files_in_directory, \
    concatenate_and_fill_dfs
from utils.handler.validate import validate_metadata, validate_extract_and_mapper, load_metrics, validate_metrics
from utils.logs.log import Logger

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

config = Config()

# print(config)

logger = Logger("GodSight")


def process():
    parser = argparse.ArgumentParser(description="GodSight On-Chain Analysis Framework")
    parser.add_argument('command', help="Command to execute (e.g., 'add_blockchain')")
    parser.add_argument('first', help="Second Argument", nargs='?')

    args = parser.parse_args()

    if args.command == 'add-blockchain':
        if args.first:
            add_blockchain(args.first)
        else:
            logger.log_error("JSON file name is required for 'add_blockchain' command.")
            sys.exit(1)
    else:
        logger.log_error(f"Unknown command: {args.command}")
        sys.exit(1)

    # can add other commands here


def add_blockchain(file_name):
    blockchain_name = None

    try:

        metadata = read_blockchain_metadata(file_name, config.meta_path)
        if metadata is None:
            logger.log_error("Failed to read blockchain metadata.")
            return

        valid, message = validate_metadata(metadata)

        if not valid:
            logger.log_error(message)
            return
        blockchain_name = metadata['name']

        if check_blockchain_exists(metadata['name'], config):
            logger.log_info(f"Blockchain {metadata['name']} already exists in the system.")
            return

        meta_data = []
        chains = []
        mapper_data = []
        functions = []
        all_test_data = {}
        for subchain in metadata['subChains']:
            # logger.log_info(f"check {subchain['name']}")

            extract_file_path = os.path.join(config.extract_path, subchain['extract_file'] + '.py')
            mapper_file_path = os.path.join(config.mapper_path, subchain['mapper_file'] + '.py')

            final_validation, validation_message, funcs, mappings, test_data = validate_extract_and_mapper(
                extract_file_path,
                mapper_file_path,
                subchain['startDate'])

            if not final_validation:
                logger.log_error(validation_message)
                return

            all_test_data[subchain['name']] = test_data

            chain_unique_id = str(uuid.uuid4())

            meta_data.append({
                'id': chain_unique_id,
                'blockchain': metadata['name'],
                'subchain': subchain['name'],
                'start_date': subchain['startDate'],
                'description': subchain['description']
            })

            subchain_mappings = format_config_for_insertion(mappings, metadata['name'], subchain['name'])

            mapper_data.append(subchain_mappings)

            functions.append({
                'id': chain_unique_id,
                'funcs': funcs,
                'sources_files': [extract_file_path, mapper_file_path]
            })

            chains.append(subchain['name'])

        if 'default' not in chains:
            meta_data.append({
                'id': chain_unique_id,
                'blockchain': metadata['name'],
                'subchain': 'default',
                'start_date': '',
                'description': 'Default chain, representing whole chains'
            })

            test_data = concatenate_and_fill_dfs(all_test_data)

            all_test_data['default'] = test_data

        metric_path = os.path.join(config.metric_path, metadata['metrics'] + '.py')
        metric_classes = load_metrics(metric_path) # TODO: need to return new metric meta data for insertion
        metric_validation = validate_metrics(metric_classes, all_test_data)

        if not metric_validation:
            logger.log_error("Metric Validation is failed.")
            return

        insert_blockchain_metadata_and_mappings(meta_data, mapper_data, config)
        # TODO: Metric meta data insertion need to do

        output_file_path = 'src/extraction/user_functions'
        output_file = os.path.join(output_file_path, str(chain_unique_id) + '.py')

        extract_imports = [
            "from ..utils.scripts.utils.http_utils import fetch_transactions",
            "from ..utils.scripts.utils.time_utils import convert_to_gmt_timestamp"
        ]

        if write_functions_to_file(functions, output_file, extract_imports):
            print("Functions and imports written successfully.")
        else:
            print("Failed to write functions and imports.")
            raise Exception("Failed to write functions and imports.")

        metric_imports = [
            "import pandas as pd"
        ] # TODO: Here check later import for BASE Metric class

        output_file_path = 'src/metric calculation/user_metrics'
        output_file = os.path.join(output_file_path, metadata['name'] + '.py')

        if write_metric_classes_to_script(metric_classes, output_file, extract_imports, metric_imports):
            print("Functions and imports written successfully.")
        else:
            print("Failed to write functions and imports.")
            raise Exception("Failed to write functions and imports.")

        logger.log_info(f"Blockchain {metadata['name']} added successfully.")
    except Exception as e:
        if blockchain_name is not None:
            delete_blockchain_data(blockchain_name, config)
            # TODO: need to delete the records of metric table also for this blockchain
        raise Exception(e)


if __name__ == "__main__":
    try:
        test_connection(config)
        logger.log_info(f"Database is connected")
        initialize_database(config)
        process()
    except Exception as e:
        logger.log_error(e)
