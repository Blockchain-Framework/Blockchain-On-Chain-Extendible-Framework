import json
from GodSight.utils.logs.log import Logger
import os

logger = Logger("GodSight")


def read_blockchain_metadata(file_name, relative_path_from_project_root):
    file_path = os.path.join(relative_path_from_project_root, file_name)
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
