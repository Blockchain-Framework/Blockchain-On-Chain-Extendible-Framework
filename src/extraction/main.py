from utils.database.services import create_extraction_tables_if_missing, get_blockchains, get_subchains, get_id
from workflow import extract_and_store_data
from config import Config
import argparse
from datetime import datetime
from logs.log import Logger

logger = Logger("GodSight")

def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    
  
def process(config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates", nargs='+', help="The dates for processing", type=valid_date)
    args = parser.parse_args()
    
    logger.log_info(f"Processing for dates {args.dates}")
    blockchains = get_blockchains(config)
    
    for date in args.dates:
        for blockchain in blockchains:
            for subchain in subchains:
                id  = get_id(config, blockchain, subchain)
                extract_and_store_data(blockchain, subchain, date, id, config)
        
if __name__ == "__main__":
    config = Config()
    blockchains = get_blockchains(config)
    logger.log_info(f"Processing for blockchains {blockchains}")
    for blockchain in blockchains:
        subchains= get_subchains(config, blockchain)
        create_extraction_tables_if_missing(config, subchains)
        
    process(config)    

    