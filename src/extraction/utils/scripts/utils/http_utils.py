# http_utils.py
import requests
import time
from logs.log import Logger

logger = Logger("GodSight")

MAX_RETRIES = 5

def fetch_transactions(url,params, headers = {"accept": "application/json"}):
    """Fetch transactions from the API with retry mechanism."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            retries += 1
            if retries < MAX_RETRIES:
                logger.log_error("API error. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logger.log_error("Max retries reached. Exiting.")
                raise Exception("Max retries reached. Exiting.")