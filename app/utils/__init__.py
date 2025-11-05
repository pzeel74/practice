"""
Utils Layer - Helper Utilities

This module contains utility functions and helpers used across the application.

Currently includes:
- logger: Centralized logging configuration

Usage:
    from app.utils import get_logger

    logger = get_logger(__name__)
    logger.info("Application started")
"""

from .logger import get_logger

__all__ = [
    "get_logger",
]
