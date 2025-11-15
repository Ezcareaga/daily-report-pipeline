#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for ExcelGenerator."""

import sys
sys.path.append('.')
import pytest
from unittest.mock import Mock

from src.core.excel import ExcelGenerator


class TestExcelGenerator:
    
    @pytest.fixture
    def mock_config_europeo(self):
        config = Mock()
        config.get.return_value = 'europeo'
        config.getint.return_value = 2
        return config
    
    @pytest.fixture
    def mock_config_americano(self):
        config = Mock()
        config.get.return_value = 'americano'
        config.getint.return_value = 2
        return config
    
    def test_init_with_config(self, mock_config_europeo):
        generator = ExcelGenerator(mock_config_europeo)
        assert generator.number_format == 'europeo'
        assert generator.decimals == 2
    
    def test_init_without_config(self):
        generator = ExcelGenerator()
        assert generator.number_format == 'europeo'
        assert generator.decimals == 2
    
    def test_get_number_format_europeo_0_decimals(self, mock_config_europeo):
        mock_config_europeo.getint.return_value = 0
        generator = ExcelGenerator(mock_config_europeo)
        assert generator.get_number_format_string() == '#.##0'
    
    def test_get_number_format_europeo_2_decimals(self, mock_config_europeo):
        generator = ExcelGenerator(mock_config_europeo)
        assert generator.get_number_format_string() == '#.##0,00'
    
    def test_get_number_format_americano_2_decimals(self, mock_config_americano):
        generator = ExcelGenerator(mock_config_americano)
        assert generator.get_number_format_string() == '#,##0.00'