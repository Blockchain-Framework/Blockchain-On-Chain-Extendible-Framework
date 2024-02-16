import logging
from datetime import datetime


class Logger:
    def __init__(self, framework_name):
        self.framework_name = framework_name

        # Configure the logging format
        log_format = f"%(asctime)s - [%(levelname)s] - {self.framework_name} - %(message)s"
        logging.basicConfig(level=logging.INFO, format=log_format)
        self.logger = logging.getLogger(self.framework_name)

    def log_info(self, message):
        # Log an INFO message
        self.logger.info(message)

    def log_error(self, message):
        # Log an ERROR message
        self.logger.error(message)

    def log_warning(self, message):
        # Log a WARNING message
        self.logger.warning(message)

    def log_debug(self, message):
        # Log a DEBUG message
        self.logger.debug(message)
