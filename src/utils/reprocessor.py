#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Date range reprocessor for reports."""

from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass

from ..core.config import ConfigManager
from ..core.exceptions import PipelineError


@dataclass
class ProcessResult:
    """Result of reprocessing operation."""
    total: int
    successful: int
    failed: int
    skipped: int
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total == 0:
            return 0.0
        return (self.successful / self.total) * 100


class DateRangeReprocessor:
    """Handles reprocessing of date ranges for reports."""
    
    def __init__(self, config: ConfigManager, report_path: Path):
        """
        Initialize reprocessor.
        
        Args:
            config: Configuration manager
            report_path: Path to report directory
        """
        self.config = config
        self.report_path = Path(report_path)
        self.script_path = None
        self.config_path = None
    
    def validate_environment(self) -> bool:
        """
        Validate required files exist.
        
        Returns:
            bool: True if validation passes
            
        Raises:
            PipelineError: If validation fails
        """
        if not self.report_path.exists():
            raise PipelineError(f"Report path not found: {self.report_path}")
        
        self.config_path = self.report_path / 'config.ini'
        if not self.config_path.exists():
            raise PipelineError(f"Config file not found: {self.config_path}")
        
        return True

    def _calculate_date_range(self, start_date: datetime, end_date: datetime) -> int:
        """
        Calculate total days in range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            int: Total days including both dates
            
        Raises:
            PipelineError: If start_date > end_date
        """
        if start_date > end_date:
            raise PipelineError("Start date must be <= end date")
        
        return (end_date - start_date).days + 1

    def _generate_date_list(self, start_date: datetime, end_date: datetime) -> list[datetime]:
        """
        Generate list of dates in range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            list: List of datetime objects
        """
        dates = []
        current = start_date
        
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        
        return dates