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

    def generate_report(
        self,
        date: datetime,
        output_path: Path,
        headers: Optional[List[str]] = None
    ) -> int:
        """
        Generate report file from database.
        
        Args:
            date: Report date
            output_path: Where to save the file
            headers: Optional column headers
            
        Returns:
            int: Number of records processed
            
        Raises:
            PipelineError: If generation fails
        """
        if self.dry_run:
            return 0
        
        try:
            query = "SELECT * FROM reports WHERE report_date = :date"
            results = self.db.execute_query(query, {'date': date})
            
            if not results:
                return 0
            
            data = [list(row) for row in results]
            self.excel.generate_excel(data, output_path, headers)
            
            return len(data)
            
        except Exception as e:
            raise PipelineError(f"Report generation failed: {e}") from e

    def process(
        self,
        date: datetime,
        output_path: Path,
        headers: Optional[List[str]] = None,
        upload_ftp: bool = True,
        send_email: bool = True
    ) -> ProcessResult:
        """
        Execute complete report processing pipeline.
        
        Args:
            date: Report date
            output_path: Where to save report
            headers: Optional Excel headers
            upload_ftp: If True, upload to FTP
            send_email: If True, send email notification
            
        Returns:
            ProcessResult: Processing result with statistics
        """
        try:
            # Check data exists
            if not self.check_data_exists(date):
                if send_email and not self.dry_run:
                    self.email.notify_no_data(date)
                return ProcessResult(
                    success=False,
                    records_processed=0,
                    error="No data available"
                )
            
            # Generate report
            count = self.generate_report(date, output_path, headers)
            
            if count == 0:
                return ProcessResult(
                    success=False,
                    records_processed=0,
                    error="No records generated"
                )
            
            # Upload to FTP
            if upload_ftp and self.ftp and not self.dry_run:
                try:
                    with self.ftp as ftp_conn:
                        ftp_conn.upload_file(output_path)
                except Exception as e:
                    # Continue even if FTP fails
                    pass
            
            # Send success email
            if send_email and not self.dry_run:
                self.email.notify_success(date, output_path)
            
            return ProcessResult(
                success=True,
                records_processed=count,
                file_generated=output_path
            )
            
        except Exception as e:
            # Send error email
            if send_email and not self.dry_run:
                self.email.notify_error(e, date)
            
            return ProcessResult(
                success=False,
                records_processed=0,
                error=str(e)
            )