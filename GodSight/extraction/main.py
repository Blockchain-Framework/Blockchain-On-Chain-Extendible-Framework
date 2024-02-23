from GodSight.extraction.utils.database.services import create_extraction_tables_if_missing, get_blockchains, get_subchains, get_id
from .workflow import extract_and_store_data
from .config import Config
import argparse
from datetime import datetime, timedelta
from .logs.log import Logger

logger = Logger("GodSight")


def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def extract_data(date, config):
    try:
        if config is None:
            config = Config()

        blockchains = get_blockchains(config)

        for blockchain in blockchains:
            subchains = get_subchains(config, blockchain)
            create_extraction_tables_if_missing(config, subchains)
            for subchain in subchains:
                id = get_id(config, blockchain, subchain)
                extract_and_store_data(blockchain, subchain, date, id, config)

    except Exception as e:
        logger.log_error(f"Extraction failed {e}")


def extract_data_for_date_range(start_date_str, end_date_str, config):
    try:
        if config is None:
            config = Config()

        blockchains = get_blockchains(config)

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Loop from start_date to end_date, inclusive
        current_date = start_date
        while current_date <= end_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            for blockchain in blockchains:
                subchains = get_subchains(config, blockchain)
                create_extraction_tables_if_missing(config, subchains)
                for subchain in subchains:
                    id = get_id(config, blockchain, subchain)
                    extract_and_store_data(blockchain, subchain, current_date_str, id, config)
            current_date += timedelta(days=1)

    except Exception as e:
        logger.log_error(f"Extraction failed {e}")


def process(config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates", nargs='+', help="The dates for processing", type=valid_date)
    args = parser.parse_args()

    logger.log_info(f"Processing for dates {args.dates}")
    blockchains = get_blockchains(config)

    for date in args.dates:
        for blockchain in blockchains:
            for subchain in subchains:
                id = get_id(config, blockchain, subchain)
                extract_and_store_data(blockchain, subchain, date, id, config)


if __name__ == "__main__":
    config = Config()
    blockchains = get_blockchains(config)
    logger.log_info(f"Processing for blockchains {blockchains}")
    for blockchain in blockchains:
        subchains = get_subchains(config, blockchain)
        create_extraction_tables_if_missing(config, subchains)

    process(config)
