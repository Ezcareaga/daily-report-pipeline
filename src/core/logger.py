#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging configuration for the application."""

import sys
from pathlib import Path
from datetime import datetime

from loguru import logger

class LoggerSetup:
    """"Configure and manage application loggin."""

    @staticmethod
    def configure(
        name: str = "app",
        level: str = "INFO",
        dog_dir: str = "logs"
    ):

        """
        Configure logger for the application.

        Args:
            name: Logger name for file naming
            level: Minimum log level (DEBUG, INFO, WARNING, ERROR)
            log_dir: Directory to store log files
        """

        logger.remove()

        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%M%D_%H%M%S")
        log_file = log_path / f"{name}_{timestamp}.log"

        
        logger.add(
            sys.stderr,
            level=level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            colorize=True
        )

        logger.add(
            log_file,
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{function}:{line} | {message}",
            rotation="100 MB",
            retention="30 days",
            encoding="utf-8"
        )

        logger.info(f"Logging initialized. File: {log_file}")

        return logger

    def setup_logger(name: str = "pipeline", verbose: bool = False) -> logger:
        """
        Quick setup for logger.

        Args:
            name: Application name
            verbose: If True, shows DEBUG messages

        Returns: 
            Configured logger instance
        """
        level = "DEBUG" if verbose else "INFO"
        LoggerSetup.configure(name=name, level=level)
        return logger