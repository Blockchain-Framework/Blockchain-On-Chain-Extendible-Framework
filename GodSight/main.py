import argparse
import sys
import os
import uuid
from GodSight.config.config import Config
from GodSight.utils.database.db import test_connection, initialize_database
from GodSight.utils.database.services import check_blockchain_exists, insert_blockchain_metadata_and_mappings, \
    delete_blockchain_data, get_all_metrics

from GodSight.utils.handler.fileReader import read_blockchain_metadata
from GodSight.utils.handler.filerWriter import write_functions_to_file, write_metric_classes_to_script, \
    extract_and_write_class_definitions
from GodSight.utils.handler.helper import format_config_for_insertion, copy_file, delete_files_in_directory, \
    concatenate_and_fill_dfs
from GodSight.utils.handler.validate import validate_metadata, validate_extract_and_mapper, load_metrics, \
    validate_custom_metrics
from GodSight.utils.logs.log import Logger

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

logger = Logger("GodSight")


def add_blockchain(file_name):
    blockchain_name = None

    try:

        config = Config()

        test_connection(config)
        logger.log_info(f"Database is connected")
        initialize_database(config)

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

        metrics = get_all_metrics(config)

        meta_data = []
        chains = []
        mapper_data = []
        functions = []
        metric_meta = []
        metric_chain_meta = []
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

            chain_basic_metrics = subchain['metrics']

            if not all(metric in chain_basic_metrics for metric in metrics):
                logger.log_error("Unknown Basic Metric Exist")
                return

            for metric in chain_basic_metrics:
                metric_chain_meta.append({
                    'blockchain_id': chain_unique_id,
                    'blockchain': metadata['name'],
                    'sub_chain': subchain['name'],
                    'metric_name': metric
                })

        if 'default' not in chains:
            chain_unique_id = str(uuid.uuid4())
            meta_data.append({
                'id': chain_unique_id,
                'blockchain': metadata['name'],
                'subchain': 'default',
                'start_date': '1900-01-01',
                'description': 'Default chain: representing whole chains'
            })

            test_data = concatenate_and_fill_dfs(all_test_data)

            all_test_data['default'] = test_data

        logger.log_info('extract and mapping validation passed')

        metric_path = os.path.join(config.metric_path, metadata['metric_file'] + '.py')

        metric_classes, metric_meta, metric_chain_meta = load_metrics(metric_path, meta_data, metrics)
        metric_validation = validate_custom_metrics(metric_classes, all_test_data)

        if not metric_validation:
            logger.log_error("Metric Validation is failed.")
            return

        insert_blockchain_metadata_and_mappings(meta_data, mapper_data, metric_meta, metric_chain_meta, config)

        output_file_path = 'GodSight/extraction/user_functions'

        extract_imports = [
            "from utils.scripts.utils.time_utils import convert_to_gmt_timestamp",
            "from utils.scripts.utils.http_utils import fetch_transactions"
        ]

        if write_functions_to_file(functions, output_file_path, extract_imports):
            logger.log_info("Functions and imports written successfully.")
        else:
            logger.log_error("Failed to write functions and imports.")
            raise Exception("Failed to write functions and imports.")

        metric_imports = [
            "import pandas as pd",
            "from utils.model.metric import CustomMetric"
        ]

        output_file_path = 'GodSight/computation/metrics/custom/'
        output_file = os.path.join(output_file_path, metadata['name'] + '.py')

        if extract_and_write_class_definitions(metric_path, output_file, metric_imports):
            logger.log_info("Metrics and imports written successfully.")
        else:
            logger.log_error("Failed to write metrics and imports.")
            raise Exception("Failed to write metrics and imports.")

        logger.log_info(f"Blockchain {metadata['name']} added successfully.")
    except Exception as e:
        if blockchain_name is not None:
            delete_blockchain_data(blockchain_name, config)
        logger.log_error(e)


def display_info():
    print("GodSight Framework - A tool for blockchain data management.")
    # Add more information about your tool here


def print_logo():
    green_color = '\033[92m'  # ANSI escape sequence for green
    reset_color = '\033[0m'
    logo = """
   ____     ____           _ ____  _       _     _    __   __  
  / /\ \   / ___| ___   __| / ___|(_) __ _| |__ | |_  \ \  \ \ 
 / /  \ \ | |  _ / _ \ / _` \___ \| |/ _` | '_ \| __|  \ \  \ \ 
 \ \  / / | |_| | (_) | (_| |___) | | (_| | | | | |_   / /  / /
  \_\/_/   \____|\___/ \__,_|____/|_|\__, |_| |_|\__| /_/  /_/ 
                                     |___/                                         
    """
    print(f"{green_color}{logo}{reset_color}")


def main():
    # Main parser
    parser = argparse.ArgumentParser(description="GodSight Framework CLI")
    parser.add_argument('--version', action='version', version='GodSight 1.0.0',
                        help="Show the version number and exit")

    # Subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    # Sub-command: add-blockchain
    parser_add = subparsers.add_parser('add-blockchain', help='Add a blockchain file')
    parser_add.add_argument('file_path', help='Path to the blockchain JSON file')

    # Sub-command: info
    parser_info = subparsers.add_parser('info', help='Display information about GodSight')

    args = parser.parse_args()

    print_logo()

    if args.command == 'add-blockchain':
        add_blockchain(args.file_path)
    elif args.command == 'info':
        display_info()
    elif not vars(args):  # No arguments provided
        parser.print_help()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
