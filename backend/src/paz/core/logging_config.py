"""
Logging configuration for PAZ application.

Provides structured logging with support for different environments.
"""

import logging
import sys
from typing import Literal

from paz.core.constants import APP_NAME


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logging(
    level: LogLevel = "INFO",
    json_format: bool = False,
) -> logging.Logger:
    """
    Configure application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: If True, output logs in JSON format (for production)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(getattr(logging, level))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level))

    if json_format:
        # JSON format for production/cloud environments
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Optional name suffix for the logger.
              If provided, logger name will be "PAZ.{name}"

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"{APP_NAME}.{name}")
    return logging.getLogger(APP_NAME)


# Default logger instance
logger = get_logger()
