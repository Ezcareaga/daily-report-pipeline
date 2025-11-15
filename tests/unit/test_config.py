#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for ConfigManager."""

import sys
sys.path.append('.')
import pytest
from pathlib import Path
from src.core.config import ConfigManager

class TestConfigManager:

    @pytest.fixture
    def temp_config(self, tmp_path):
        config_file = tmp_path / "test_config.ini"
        config_file.write_text("""
[DATABASE]
host = localhost
port = 1521
user = testuser

[EMAIL]
enabled = true
retry = 3
""")

        return config_file

    def test_load_valid_config(self, temp_config):
        config = ConfigManager(str(temp_config))
        assert config.get('DATABASE', 'host') == 'localhost'

    def test_get_with_default(self, temp_config):
        config = ConfigManager(str(temp_config))
        assert config.get('DATABASE', 'missing', 'default') == 'default'

    def test_getint(self, temp_config):
        config = ConfigManager(str(temp_config))
        assert config.getint('DATABASE', 'port') == 1521
        assert isinstance(config.getint('DATABASE', 'port'), int)

    def test_getboolean(self, temp_config):
        config = ConfigManager(str(temp_config))
        assert config.getboolean('EMAIL', 'enabled') is True

    def test_missing_file_raises_error(self):
        with pytest.raises(FileNotFoundError):
            ConfigManager('nonexistent.ini')