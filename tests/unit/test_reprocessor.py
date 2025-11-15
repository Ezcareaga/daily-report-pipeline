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