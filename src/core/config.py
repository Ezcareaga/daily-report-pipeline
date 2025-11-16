#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Configuration managemnt module."""

import configparser
from pathlib import Path
from typing import Optional

class ConfigManager:
    """Handles configuration files operations."""

    def __init__(self, config_path: str = "config.ini"):
        """
        Initialize configuration manager.

        ARGS:
            config_path: Path to configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
        """

        self.path = Path(config_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        self.config = configparser.ConfigParser()
        self.config.read(self.path, encoding='utf-8')

    def get(self, section: str, key, default: Optional[str]= None)-> str:
        """Get string value from config."""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if default is not None:
                return default
            raise

    def getint(self, section: str, key: str, default: Optional[int] = None) -> int:
        """Get integer value from config."""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if default is not None:
                return default
            raise

    def getboolean(self, section: str, key: str, default: Optional[bool] = None) -> bool:
        """Get boolean value from config."""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if default is not None:
                return default
            raise

    def has_section(self, section: str) -> bool:
        """Check if section exists."""
        return self.config.has_section(section)