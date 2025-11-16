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