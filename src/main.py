import argparse
import sys
import os
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from utils import *
from config import Config

config = Config()

logger = Logger("GodSight")

def process():
    parser = argparse.ArgumentParser(description="GodSight On-Chain Analysis Framework")
    parser.add_argument('command', help="Command to execute (e.g., 'add_blockchain')")
    parser.add_argument('first', help="Second Argument", nargs='?')
    
    args = parser.parse_args()

    if args.command == 'add_blockchain':
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
    logger.log_info("check 1")
    metadata = read_blockchain_metadata(file_name, config.meta_path)
    if metadata is None:
        logger.log_error("Failed to read blockchain metadata.")
        return
    logger.log_info("check 2")
    valid, message = validate_metadata(metadata)
    logger.log_info("check 3")
    if not valid:
        logger.log_error(message)
        return
    logger.log_info("check 4")
    if check_blockchain_exists(metadata['name'], config):
        return False, f"Blockchain {metadata['name']} already exists in the system."
    logger.log_info("check 5")
    meta_data = []
    mapper_data = []
    funcs = []
    logger.log_info("check 6")
    for subchain in metadata['subChains']:
        logger.log_info(f"check {subchain['name']}")
        extract_validation_passed, mapper_validation_passed, extract_validation_message, mapper_validation_message, mappings, functions = validate_extract_and_mapper(subchain['extract_file'], subchain['mapper_file'], config.extract_path, config.mapper_path, subchain['startDate'])

        if not extract_validation_passed:
            logger.log_error(extract_validation_message)
            return
        
        if not mapper_validation_passed:
            logger.log_error(mapper_validation_message)
            return
        
        chain_unique_id = str(uuid.uuid4())
        
        meta_data.append({
            'id': chain_unique_id,
            'blockchain': metadata['name'],
            'subchain': subchain['name'],
            'start_date': subchain['start_date'],
            'description': subchain['description']
        })

        subchain_mappings = format_config_for_insertion(mappings,  metadata['name'], subchain['name'])
        mapper_data.append(subchain_mappings)

        funcs.append({
            'id': chain_unique_id,
            'funcs': functions,
            'sources_files': [config.extract_path + subchain['extract_file'] , config.mapper_path + subchain['mapper_file']]
        })
    
    insert_blockchain_metadata_and_mappings(meta_data, mapper_data, config)
    output_path = 'src\\extraction\\user_functions'
    write_functions_to_new_scripts(funcs, output_path)
    logger.log_info(f"Blockchain {metadata['name']} added successfully.")

if __name__ == "__main__":
    try:
        test_connection(config)
        logger.log_info(f"Database is connected")
        initialize_database(config)
        process()
    except Exception as e:
        logger.log_error(e)

