import os
import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root
import datetime
import yaml
from src.constants import CONFIG_PATH, LOG_PATH, MAX_LOG_SIZE

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

LOG_DIR = LOG_PATH

LOG_LEVEL = config["logging"]["level"]
LOG_FORMAT = config["logging"]["format"]
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir_path = os.path.join(from_root(), LOG_DIR)
log_file_path = os.path.join(log_dir_path, LOG_FILE)



def configure_logger():
    """
    Function to configure logger to enable logging via console handler and file handler.
    """

    # make logging directory
    os.makedirs(LOG_DIR, exist_ok=True)

    # initiate logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # console logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(LOG_LEVEL)

    # file logger
    file_logger = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE)
    file_logger.setLevel(LOG_LEVEL)

    # set formatters
    console_logger.setFormatter(LOG_FORMAT)
    file_logger.setFormatter(LOG_FORMAT)

    # add handlers
    logger.addHandler(console_logger)
    logger.addHandler(file_logger)


configure_logger()