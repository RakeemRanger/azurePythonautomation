import logging
import os
import json

from autocli.lib.CONSTANTS import log_folder

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Optionally add more fields from record if needed
        return json.dumps(log_record)

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
        formatter = JsonFormatter()
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger