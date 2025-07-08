import logging
import os

def logClient(logName: str) -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(__file__), '/home/nodebrite/Desktop/AzureAutomatioin/src/autocli/autocli/cli/logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{logName}.log")
    logger = logging.getLogger(f'{logName}.log')
    logger.setLevel(logging.INFO)
    # Prevent adding multiple handlers if logger is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger