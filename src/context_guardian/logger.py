"""Logging configuration for Context Guardian."""

import logging
import sys


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Set up a logger with consistent formatting.

    Args:
        name: Logger name (typically __name__).
        level: Logging level as string ('DEBUG', 'INFO', 'WARNING', 'ERROR').

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Don't reconfigure if already has handlers
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())

    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level.upper())

    formatter = logging.Formatter(
        fmt="%(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """Get or create a logger.

    Args:
        name: Logger name.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
