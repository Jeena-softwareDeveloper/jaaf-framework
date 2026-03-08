import logging
import os
from datetime import datetime

# Centralized Logging Configuration for JAAF Professional AI
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE = os.path.join(LOGS_DIR, "jaaf_master.log")

def setup_logger(name="jaaf"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(name)s | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(asctime)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
    
    return logger

# Singleton JAAF Logger
jaaf_logger = setup_logger("jaaf")
