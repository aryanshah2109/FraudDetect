import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from from_root import from_root

from src.config import config_loader
from src.path_constants import LOG_PATH, MAX_LOG_SIZE

config = config_loader.load_config()

LOG_DIR = LOG_PATH

LOG_LEVEL = getattr(logging, config["logging"]["level"])
LOG_FORMAT = logging.Formatter(config["logging"]["format"])
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir_path = os.path.join(from_root(), LOG_DIR)
log_file_path = os.path.join(log_dir_path, LOG_FILE)



def configure_logger():
    """
    Function to configure logger to enable logging via console handler and file handler.
    """

    try:

        logging.info("Creating and setting up logger object.")
        # make logging directory
        os.makedirs(LOG_DIR, exist_ok=True)

        # initiate logger
        logger = logging.getLogger()
        logger.setLevel(LOG_LEVEL)

        # Remove existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()

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

    except Exception as e:
        logging.error(f"Error while creating logger object : {e}")
        raise



configure_logger()