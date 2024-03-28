"""
    Build and customize a console and file logger.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from constants import DEFAULT_LOG_FILE, DEFAULT_LOG_LEVELS, LOG_LEVELS, FORMATTER, CONSOLE_FORMATTER


def get_logger(name: str) -> logging.Logger:
    """
    Creates a basic logger to use throughout the application.

    Args:
        name (str): logger name.

    Returns:
        Logger: logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set lowest log level

    # Create file handler that will always log debug messages
    __set_logfile(DEFAULT_LOG_FILE)
    fh = RotatingFileHandler(DEFAULT_LOG_FILE, backupCount=5, maxBytes=1000000)
    fh.setLevel(LOG_LEVELS[DEFAULT_LOG_LEVELS["file_loglevel"]])

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVELS[DEFAULT_LOG_LEVELS["console_loglevel"]])

    # Apply the same format to both console and file handlers
    fh.setFormatter(FORMATTER)
    ch.setFormatter(CONSOLE_FORMATTER)

    # Add handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger


def __set_logfile(new_file):
    """
    Set a new specific file to store applications logs.

    Args:
        new_file (str): path to the log file.
    """
    if not os.path.exists(new_file):
        Path(new_file).parent.mkdir(parents=True, exist_ok=True)
        with open(new_file, "w+", encoding="utf-8"):
            pass  # Just to check that the file is present and working


def set_loglevel(logger, new_level: str):
    """
    Customize logger level.

    Args:
        logger (logger): logger handler to modify.
        new_level (str): new log level to apply.
    """
    logger.handlers[0].setLevel(new_level)
    DEFAULT_LOG_LEVELS["console_loglevel"] = new_level