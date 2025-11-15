#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Email notification management."""

import smtplib
from pathlib import Path
from email.message import EmailMessage
from typing import List, Optional
from datetime import datetime

from .config import ConfigManager
from .exceptions import PipelineError


class EmailManager:
    """Handles email notifications for reports."""
    
    def __init__(self, config: ConfigManager):
        """
        Initialize email manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.enabled = config.getboolean('EMAIL', 'habilitado', default=False)
        
        if self.enabled:
            self.server = config.get('EMAIL', 'servidor_smtp')
            self.port = config.getint('EMAIL', 'puerto_smtp')
            self.sender = config.get('EMAIL', 'remitente_email')
            self.password = config.get('EMAIL', 'remitente_password', default='')
            self.use_ssl = config.getboolean('EMAIL', 'usar_ssl', default=False)
            self.max_attachment_mb = config.getint('EMAIL', 'max_tamano_adjunto_mb', default=10)
            
            recipients_str = config.get('EMAIL', 'destinatarios_principales')
            self.recipients_success = [r.strip() for r in recipients_str.split(',')]
            
            error_recipients = config.get('EMAIL', 'destinatarios_error', default=None)
            if error_recipients:
                self.recipients_error = [r.strip() for r in error_recipients.split(',')]
            else:
                self.recipients_error = self.recipients_success
    
    def validate_attachment_size(self, file_path: Path) -> bool:
        """
        Validate attachment file size.
        
        Args:
            file_path: Path to file
            
        Returns:
            bool: True if size is within limits
            
        Raises:
            PipelineError: If file exceeds size limit
        """
        if not file_path.exists():
            raise PipelineError(f"Attachment not found: {file_path}")
        
        size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if size_mb > self.max_attachment_mb:
            raise PipelineError(
                f"Attachment size ({size_mb:.2f}MB) exceeds limit ({self.max_attachment_mb}MB)"
            )
        
        return True