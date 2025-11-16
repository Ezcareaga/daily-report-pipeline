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

    def _send_email(
        self,
        subject: str,
        html_body: str,
        recipients: List[str],
        attachment_path: Optional[Path] = None
    ) -> bool:
        """
        Send email with optional attachment.
        
        Args:
            subject: Email subject
            html_body: HTML body content
            recipients: List of recipient emails
            attachment_path: Optional file to attach
            
        Returns:
            bool: True if sent successfully
            
        Raises:
            PipelineError: If sending fails
        """
        if not self.enabled:
            return False
        
        if attachment_path:
            self.validate_attachment_size(attachment_path)
        
        try:
            msg = EmailMessage()
            msg['From'] = self.sender
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            
            msg.set_content("This email requires an HTML-capable client.")
            msg.add_alternative(html_body, subtype='html')
            
            if attachment_path:
                with open(attachment_path, 'rb') as f:
                    msg.add_attachment(
                        f.read(),
                        maintype='application',
                        subtype='octet-stream',
                        filename=attachment_path.name
                    )
            
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.server, self.port) as server:
                    if self.password:
                        server.login(self.sender, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.server, self.port) as server:
                    if self.password:
                        server.login(self.sender, self.password)
                    server.send_message(msg)
            
            return True
            
        except Exception as e:
            raise PipelineError(f"Failed to send email: {e}") from e

    def notify_success(
        self,
        date: datetime,
        attachment_path: Optional[Path] = None,
        total_amount: Optional[float] = None
    ) -> bool:
        """
        Send success notification.
        
        Args:
            date: Report date
            attachment_path: Optional file to attach
            total_amount: Optional total amount processed
            
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            return False
        
        subject = self.config.get(
            'EMAIL', 
            'asunto_exito', 
            default='Report Success - {fecha}'
        ).format(fecha=date.strftime('%Y-%m-%d'))
        
        filename = attachment_path.name if attachment_path else "No attachment"
        
        body = self.config.get(
            'EMAIL',
            'cuerpo_exito',
            default='<p>Report generated successfully for {fecha}</p><p>File: {archivo}</p>'
        ).format(
            fecha=date.strftime('%d/%m/%Y'),
            archivo=filename
        )
        
        if total_amount is not None:
            body += f'<br><br><b>Total Amount:</b> {total_amount:,.2f}'
        
        return self._send_email(subject, body, self.recipients_success, attachment_path)
    
    def notify_no_data(self, date: datetime) -> bool:
        """
        Send notification when no data available.
        
        Args:
            date: Report date
            
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            return False
        
        subject = self.config.get(
            'EMAIL',
            'asunto_sin_datos',
            default='No Data - {fecha}'
        ).format(fecha=date.strftime('%Y-%m-%d'))
        
        body = self.config.get(
            'EMAIL',
            'cuerpo_sin_datos',
            default='<p>No data available for {fecha}</p>'
        ).format(fecha=date.strftime('%d/%m/%Y'))
        
        return self._send_email(subject, body, self.recipients_error)
    
    def notify_error(
        self,
        error: Exception,
        date: datetime,
        include_traceback: bool = True
    ) -> bool:
        """
        Send error notification.
        
        Args:
            error: Exception that occurred
            date: Report date
            include_traceback: Include full traceback
            
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            return False
        
        subject = self.config.get(
            'EMAIL',
            'asunto_error',
            default='Error - {fecha}'
        ).format(fecha=date.strftime('%Y-%m-%d'))
        
        error_details = str(error)
        if include_traceback:
            import traceback
            error_details += f'\n\n{traceback.format_exc()}'
        
        body = self.config.get(
            'EMAIL',
            'cuerpo_error',
            default='<p>Error occurred on {fecha}</p><p>{error}</p><pre>{traceback}</pre>'
        ).format(
            fecha=date.strftime('%d/%m/%Y'),
            error=error,
            traceback=error_details
        )
        
        return self._send_email(subject, body, self.recipients_error)