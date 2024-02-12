import argparse
import sys
import os
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from utils import *
from blockchains import *
from config import Config

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
        mapper_data = []
        funcs = []
        for subchain in metadata['subChains']:
            # logger.log_info(f"check {subchain['name']}")

            extract_file_path = os.path.join(os.getcwd(),config.extract_path, subchain['extract_file']+'.py')
            mapper_file_path = os.path.join(os.getcwd(),config.mapper_path, subchain['mapper_file']+'.py')

            # print(extract_file_path, mapper_file_path)

            final_validation, validation_message, funcs, mappings = validate_extract_and_mapper(extract_file_path, mapper_file_path, subchain['startDate'])

            if not final_validation:
                logger.log_error(validation_message)
                return
            
            chain_unique_id = str(uuid.uuid4())
            
            meta_data.append({
                'id': chain_unique_id,
                'blockchain': metadata['name'],
                'subchain': subchain['name'],
                'start_date': subchain['startDate'],
                'description': subchain['description']
            })

            subchain_mappings = format_config_for_insertion(mappings,  metadata['name'], subchain['name'])
            mapper_data.append(subchain_mappings)

            funcs.append({
                'id': chain_unique_id,
                'funcs': funcs,
                'sources_files': [extract_file_path, mapper_file_path]
            })

        
        insert_blockchain_metadata_and_mappings(meta_data, mapper_data, config)
        output_path = 'extraction\\user_functions'
        print(funcs)
        # combine_scripts_ignore_imports(funcs, output_path)
        logger.log_info(f"Blockchain {metadata['name']} added successfully.")
    except Exception as e:
        if not blockchain_name is None:
            delete_blockchain_data(blockchain_name, config)
        raise Exception(e)
             
if __name__ == "__main__":
    try:
        test_connection(config)
        logger.log_info(f"Database is connected")
        initialize_database(config)
        process()
    except Exception as e:
        logger.log_error(e)

