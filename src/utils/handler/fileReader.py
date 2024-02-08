import json
from ..logs import Logger

logger = Logger("GodSight")

def read_blockchain_metadata(file_name, path):

    file_path = path + file_name
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        logger.log_error("File not found.")
        raise Exception(e)
    except json.JSONDecodeError as e:
        logger.log_error("Error decoding JSON.")
        raise Exception(e)
    except Exception as e:
        logger.log_error(f"An error occurred: {e}")
        raise Exception(e)
