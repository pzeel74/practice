"""
Logger Utility

Provides centralized logging configuration for the application.
Replaces print() statements with proper logging for production.

Usage:
    from app.utils import get_logger

    logger = get_logger(__name__)
    logger.info("Processing book...")
    logger.error("Failed to process book", exc_info=True)
"""

import logging
import sys
from typing import Optional


def get_logger(
    name: str,
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Get or create a configured logger.

    Args:
        name: Logger name (typically __name__ of the module)
        level: Logging level (default: logging.INFO)
        format_string: Custom format string (optional)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Only configure if no handlers exist (avoid duplicate handlers)
    if not logger.handlers:
        logger.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter
        if format_string is None:
            format_string = (
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

        formatter = logging.Formatter(format_string)
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger


def setup_application_logging(level: int = logging.INFO):
    """
    Setup application-wide logging configuration.

    Call this once at application startup in main.py.

    Args:
        level: Logging level for the entire application
    """
    # Configure root logger
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set specific log levels for third-party libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("pinecone").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
