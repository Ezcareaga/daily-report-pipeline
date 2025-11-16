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

    def test_generate_report_success(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.execute_query.return_value = [
            (1, 'Test', 100.50),
            (2, 'Another', 200.75)
        ]
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        count = processor.generate_report(date, output, ['ID', 'Name', 'Value'])
        
        assert count == 2
        excel.generate_excel.assert_called_once()
    
    def test_generate_report_no_data(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.execute_query.return_value = []
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        count = processor.generate_report(date, output)
        
        assert count == 0
        excel.generate_excel.assert_not_called()
    
    def test_generate_report_dry_run(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        config.getboolean.return_value = True  # dry_run = True
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        count = processor.generate_report(date, output)
        
        assert count == 0
        db.execute_query.assert_not_called()

    def test_process_success_complete(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.check_data_exists.return_value = (True, 100)
        db.execute_query.return_value = [(1, 'Test', 100.50)]
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        result = processor.process(date, output)
        
        assert result.success is True
        assert result.records_processed == 1
        assert result.file_generated == output
        email.notify_success.assert_called_once()
    
    def test_process_no_data(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.check_data_exists.return_value = (False, 0)
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        result = processor.process(date, output)
        
        assert result.success is False
        assert result.records_processed == 0
        assert result.error == "No data available"
        email.notify_no_data.assert_called_once()
    
    def test_process_skip_email_and_ftp(self, mock_components, tmp_path):
        from datetime import datetime
        
        config, db, email, excel, ftp = mock_components
        db.check_data_exists.return_value = (True, 50)
        db.execute_query.return_value = [(1, 'Test')]
        
        processor = ReportProcessor(config, db, email, excel, ftp)
        output = tmp_path / "report.xlsx"
        date = datetime(2025, 1, 15)
        
        result = processor.process(date, output, upload_ftp=False, send_email=False)
        
        assert result.success is True
        email.notify_success.assert_not_called()