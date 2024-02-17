import argparse
from datetime import datetime
import sys
import os
import uuid
from config import Config
from utils.database.db import test_connection, initialize_database
from utils.database.services import get_all_metrics, create_metric_tables_if_not_exist
from workflow import MetricCalculationWorkflowManager
from logs.log import Logger

logger = Logger("GodSight")

def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def create_metric_tables(config):
    metrics = get_all_metrics(config)
    create_metric_tables_if_not_exist(metrics, config)
    logger.log_info(f"Metric tables created successfully")
    
def process(config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates", nargs='+', help="The dates for processing", type=valid_date)
    args = parser.parse_args()
    
    print(args.dates)
    
    manager = MetricCalculationWorkflowManager()
    for i in args.dates:
        manager.run_workflow(i)

if __name__ == "__main__":
    config = Config()
    test_connection(config)
    logger.log_info(f"Database is connected")
    create_metric_tables(config)
    process(config)
