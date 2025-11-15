#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Excel file generation utilities."""

from pathlib import Path
from typing import List, Any, Optional
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font

from .config import ConfigManager
from .exceptions import PipelineError


class ExcelGenerator:
    """Handles Excel file generation with custom formatting."""
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize Excel generator.
        
        Args:
            config: Optional configuration manager
        """
        self.config = config
        
        if config:
            self.number_format = config.get('ARCHIVOS', 'formato_numero', default='europeo')
            self.decimals = config.getint('ARCHIVOS', 'decimales', default=2)
        else:
            self.number_format = 'europeo'
            self.decimals = 2
    
    def get_number_format_string(self) -> str:
        """
        Get Excel number format string based on configuration.
        
        Returns:
            str: Excel number format string
        """
        if self.number_format == 'europeo':
            if self.decimals == 0:
                return '#.##0'
            elif self.decimals == 1:
                return '#.##0,0'
            elif self.decimals == 2:
                return '#.##0,00'
            else:
                return '#.##0,' + '0' * self.decimals
        else:
            if self.decimals == 0:
                return '#,##0'
            elif self.decimals == 1:
                return '#,##0.0'
            elif self.decimals == 2:
                return '#,##0.00'
            else:
                return '#,##0.' + '0' * self.decimals