#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for ReportProcessor."""

import sys
sys.path.append('.')
import pytest
from unittest.mock import Mock
from pathlib import Path

from src.reports.processor import ReportProcessor, ProcessResult


class TestProcessResult:
    
    def test_process_result_success(self):
        result = ProcessResult(
            success=True,
            records_processed=100,
            file_generated=Path("report.xlsx")
        )
        assert result.success is True
        assert result.records_processed == 100
        assert result.file_generated == Path("report.xlsx")
        assert result.error is None


class TestReportProcessor:
    
    @pytest.fixture
    def mock_components(self):
        config = Mock()
        config.getboolean.return_value = False
        
        db = Mock()
        email = Mock()
        excel = Mock()
        ftp = Mock()
        
        return config, db, email, excel, ftp
    
    def test_init(self, mock_components):
        config, db, email, excel, ftp = mock_components
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        
        assert processor.config == config
        assert processor.db == db
        assert processor.email == email
        assert processor.excel == excel
        assert processor.ftp == ftp
        assert processor.dry_run is False

    def test_check_data_exists_true(self, mock_components):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.check_data_exists.return_value = (True, 100)
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        date = datetime(2025, 1, 15)
        
        assert processor.check_data_exists(date) is True
        db.check_data_exists.assert_called_once_with(date)
    
    def test_check_data_exists_false(self, mock_components):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.check_data_exists.return_value = (False, 0)
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        date = datetime(2025, 1, 15)
        
        assert processor.check_data_exists(date) is False