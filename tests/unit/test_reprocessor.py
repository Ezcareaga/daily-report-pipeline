#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for DateRangeReprocessor."""

import sys
sys.path.append('.')
import pytest
from pathlib import Path
from unittest.mock import Mock

from src.utils.reprocessor import DateRangeReprocessor, ProcessResult
from src.core.exceptions import PipelineError


class TestProcessResult:
    
    def test_success_rate_calculation(self):
        result = ProcessResult(total=10, successful=8, failed=2, skipped=0)
        assert result.success_rate == 80.0
    
    def test_success_rate_zero_total(self):
        result = ProcessResult(total=0, successful=0, failed=0, skipped=0)
        assert result.success_rate == 0.0


class TestDateRangeReprocessor:
    
    @pytest.fixture
    def mock_config(self):
        return Mock()
    
    @pytest.fixture
    def temp_report_path(self, tmp_path):
        report_dir = tmp_path / "test_report"
        report_dir.mkdir()
        (report_dir / "config.ini").write_text("[TEST]\nvalue=1")
        return report_dir
    
    def test_init(self, mock_config, temp_report_path):
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        assert reprocessor.config == mock_config
        assert reprocessor.report_path == temp_report_path
    
    def test_validate_environment_success(self, mock_config, temp_report_path):
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        assert reprocessor.validate_environment() is True
    
    def test_validate_environment_missing_path(self, mock_config, tmp_path):
        nonexistent = tmp_path / "nonexistent"
        reprocessor = DateRangeReprocessor(mock_config, nonexistent)
        
        with pytest.raises(PipelineError, match="Report path not found"):
            reprocessor.validate_environment()
    
    def test_validate_environment_missing_config(self, mock_config, tmp_path):
        report_dir = tmp_path / "test_report"
        report_dir.mkdir()
        reprocessor = DateRangeReprocessor(mock_config, report_dir)
        
        with pytest.raises(PipelineError, match="Config file not found"):
            reprocessor.validate_environment()

    def test_calculate_date_range_valid(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 5)
        
        assert reprocessor._calculate_date_range(start, end) == 5
    
    def test_calculate_date_range_same_day(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        date = datetime(2025, 1, 1)
        
        assert reprocessor._calculate_date_range(date, date) == 1
    
    def test_calculate_date_range_invalid(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        start = datetime(2025, 1, 5)
        end = datetime(2025, 1, 1)
        
        with pytest.raises(PipelineError, match="Start date must be"):
            reprocessor._calculate_date_range(start, end)

    def test_generate_date_list(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 3)
        
        dates = reprocessor._generate_date_list(start, end)
        
        assert len(dates) == 3
        assert dates[0] == datetime(2025, 1, 1)
        assert dates[1] == datetime(2025, 1, 2)
        assert dates[2] == datetime(2025, 1, 3)

    def test_reprocess_range_success(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        processed_dates = []
        def mock_processor(date):
            processed_dates.append(date)
        
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 3)
        
        result = reprocessor.reprocess_range(start, end, mock_processor)
        
        assert result.total == 3
        assert result.successful == 3
        assert result.failed == 0
        assert len(processed_dates) == 3
    
    def test_reprocess_range_with_failures(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        call_count = 0
        def failing_processor(date):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise Exception("Simulated failure")
        
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 3)
        
        result = reprocessor.reprocess_range(start, end, failing_processor)
        
        assert result.total == 3
        assert result.successful == 2
        assert result.failed == 1
    
    def test_reprocess_range_dry_run(self, mock_config, temp_report_path):
        from datetime import datetime
        reprocessor = DateRangeReprocessor(mock_config, temp_report_path)
        
        processed = []
        def mock_processor(date):
            processed.append(date)
        
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 3)
        
        result = reprocessor.reprocess_range(start, end, mock_processor, dry_run=True)
        
        assert result.total == 3
        assert result.skipped == 3
        assert len(processed) == 0