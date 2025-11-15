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

    def test_create_workbook_without_headers(self):
        generator = ExcelGenerator()
        data = [
            [1, 'Test', 123.45],
            [2, 'Another', 678.90]
        ]
        
        wb = generator.create_workbook(data)
        ws = wb.active
        
        assert ws.cell(1, 1).value == 1
        assert ws.cell(1, 2).value == 'Test'
        assert ws.cell(2, 1).value == 2
    
    def test_create_workbook_with_headers(self):
        generator = ExcelGenerator()
        headers = ['ID', 'Name', 'Amount']
        data = [[1, 'Test', 123.45]]
        
        wb = generator.create_workbook(data, headers=headers)
        ws = wb.active
        
        assert ws.cell(1, 1).value == 'ID'
        assert ws.cell(1, 2).value == 'Name'
        assert ws.cell(1, 3).value == 'Amount'
        assert ws.cell(1, 1).font.bold is True
        assert ws.cell(2, 1).value == 1
    
    def test_create_workbook_with_datetime(self):
        from datetime import datetime
        generator = ExcelGenerator()
        
        date_val = datetime(2025, 1, 15, 10, 30, 0)
        data = [[date_val]]
        
        wb = generator.create_workbook(data)
        ws = wb.active
        
        assert ws.cell(1, 1).value == date_val
        assert ws.cell(1, 1).number_format == 'YYYY-MM-DD HH:MM:SS'
    
    def test_save_workbook(self, tmp_path):
        generator = ExcelGenerator()
        data = [[1, 'Test']]
        wb = generator.create_workbook(data)
        
        file_path = tmp_path / "test.xlsx"
        generator.save_workbook(wb, file_path)
        
        assert file_path.exists()