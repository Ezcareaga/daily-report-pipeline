#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
processor.py
============
Main report processing orchestrator.

Coordinates all components to generate, deliver and track reports:
- Data validation and extraction
- File generation (Excel/text)
- Compression
- Email notifications  
- FTP transfers

Author: Alberto Careaga
Version: 1.0
Python: 3.8+
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, List, Any
from dataclasses import dataclass

from ..core.config import ConfigManager
from ..core.database import DatabaseManager
from ..core.email import EmailManager
from ..core.excel import ExcelGenerator
from ..core.ftp import FTPManager
from ..core.exceptions import PipelineError


@dataclass
class ProcessResult:
    """Result of report processing."""
    success: bool
    records_processed: int
    file_generated: Optional[Path] = None
    error: Optional[str] = None


class ReportProcessor:
    """Orchestrates the complete report generation pipeline."""
    
    def __init__(
        self,
        config: ConfigManager,
        db_manager: DatabaseManager,
        email_manager: EmailManager,
        excel_generator: ExcelGenerator,
        ftp_manager: Optional[FTPManager] = None
    ):
        """
        Initialize report processor.
        
        Args:
            config: Configuration manager
            db_manager: Database manager
            email_manager: Email manager
            excel_generator: Excel generator
            ftp_manager: Optional FTP manager
        """
        self.config = config
        self.db = db_manager
        self.email = email_manager
        self.excel = excel_generator
        self.ftp = ftp_manager
        self.dry_run = config.getboolean('MODO', 'dry_run', default=False)

    def check_data_exists(self, date: datetime) -> bool:
        """
        Check if data exists for given date.
        
        Args:
            date: Date to check
            
        Returns:
            bool: True if data exists
            
        Raises:
            PipelineError: If check fails
        """
        try:
            exists, count = self.db.check_data_exists(date)
            return exists
        except Exception as e:
            raise PipelineError(f"Failed to check data: {e}") from e