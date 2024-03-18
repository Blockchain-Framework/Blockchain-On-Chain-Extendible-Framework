import argparse
from datetime import datetime, timedelta
import sys
import os
import uuid
from config import Config
from computation.utils.database.db import test_connection, initialize_database
from computation.utils.database.services import get_all_metrics, create_metric_tables_if_not_exist
from .workflow import MetricCalculationWorkflowManager
from .logs.log import Logger

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


def compute_data(date_str, config):
    try:
        if config is None:
            config = Config()

        create_metric_tables(config)

        manager = MetricCalculationWorkflowManager()
        manager.run_workflow(date_str, config)

    except Exception as e:
        logger.log_error(f"Extraction failed {e}")


def compute_data_for_date_range(start_date_str, end_date_str, config):
    try:
        if config is None:
            config = Config()

        manager = MetricCalculationWorkflowManager()

        create_metric_tables(config)

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Loop from start_date to end_date, inclusive
        current_date = start_date
        while current_date <= end_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            manager.run_workflow(current_date_str, config)
            current_date += timedelta(days=1)

    except Exception as e:
        logger.log_error(f"Extraction failed {e}")


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
