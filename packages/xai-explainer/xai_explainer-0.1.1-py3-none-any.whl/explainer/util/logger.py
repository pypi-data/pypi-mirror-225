from collections import OrderedDict
import json
import logging
import logging.config
import os
from pathlib import Path
from typing import Union


def _logging_config() -> dict:
    """Create basic configuration for logging.

    Returns:
        dict: Configuration-dict.
    """
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "screen": {
                "format": "[%(asctime)s] [%(levelname)s] [%(filename)s():%(lineno)s] - %(message)s",  # noqa: E501
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "full": {
                "format": "[%(asctime)s] [%(levelname)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "screen_handler": {
                "level": "WARNING",
                "formatter": "screen",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {"handlers": ["screen_handler"], "level": "DEBUG", "propagate": False}
        },
    }


def _init_logger():
    """Initialize logger."""
    log_config_dict = _logging_config()
    log_config_dict["handlers"]["screen_handler"]["level"] = "WARNING"
    logging.config.dictConfig(log_config_dict)


def set_logging_level(level: Union[int, str]) -> None:
    """Set logging level.

    Args:
        level (Union[int, str]): Logging level. Possible values are
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
    """
    if isinstance(level, str):
        level = level.upper()
    else:
        level = logging.getLevelName(level)
    try:
        log_config_dict = _logging_config()
        log_config_dict["handlers"]["screen_handler"]["level"] = level
        logging.config.dictConfig(log_config_dict)
    except ValueError:
        # default to WARNING
        set_logging_level("WARNING")
        logging.error(f"Logging level {level} is not a valid input!")


_init_logger()
