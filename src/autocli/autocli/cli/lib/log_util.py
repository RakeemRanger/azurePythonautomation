import logging
import os

from src.autocli.autocli.cli.lib.CONSTANTS import log_folder

def logClient(logName: str) -> logging.Logger:
    log_directory = log_folder
    log_dir = os.path.join(os.path.dirname(__file__), str(log_directory))
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{logName}.log")
    logger = logging.getLogger(f'{logName}.log')
    logger.setLevel(logging.INFO)
    # Prevent adding multiple handlers if logger is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        # Remove trackingId from formatter to avoid KeyError
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger