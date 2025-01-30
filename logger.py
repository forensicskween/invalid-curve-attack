import logging
import sys
from typing import Optional

def setup_logger(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Configures the logger to print messages to the console and optionally save to a log file.

    Args:
        level (int): The logging level (default: `logging.INFO`).
        log_file (Optional[str]): If provided, logs will be written to this file.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create console handler (prints to terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file, mode='a')  # Append mode
        file_handler.setLevel(level)
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.info(f"Logger initialized at level {logging.getLevelName(level)}")
    if log_file:
        logger.info(f"Logging to file: {log_file}")

    return logger  # Return logger in case module-level logging is needed
