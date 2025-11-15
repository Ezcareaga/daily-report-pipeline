#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for EmailManager."""

import sys
sys.path.append('.')
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.email import EmailManager
from src.core.exceptions import PipelineError


class TestEmailManager:
    
    @pytest.fixture
    def mock_config_enabled(self):
        config = Mock()
        config.getboolean.side_effect = lambda section, key, default=False: {
            ('EMAIL', 'habilitado'): True,
            ('EMAIL', 'usar_ssl'): False
        }.get((section, key), default)
        
        config.get.side_effect = lambda section, key, default=None: {
            ('EMAIL', 'servidor_smtp'): 'smtp.test.com',
            ('EMAIL', 'remitente_email'): 'test@test.com',
            ('EMAIL', 'remitente_password'): 'password',
            ('EMAIL', 'destinatarios_principales'): 'user1@test.com,user2@test.com'
        }.get((section, key), default)
        
        config.getint.side_effect = lambda section, key, default=0: {
            ('EMAIL', 'puerto_smtp'): 587,
            ('EMAIL', 'max_tamano_adjunto_mb'): 10
        }.get((section, key), default)
        
        return config
    
    @pytest.fixture
    def mock_config_disabled(self):
        config = Mock()
        config.getboolean.return_value = False
        return config
    
    def test_init_enabled(self, mock_config_enabled):
        email = EmailManager(mock_config_enabled)
        assert email.enabled is True
        assert email.server == 'smtp.test.com'
        assert email.port == 587
        assert email.sender == 'test@test.com'
        assert len(email.recipients_success) == 2
    
    def test_init_disabled(self, mock_config_disabled):
        email = EmailManager(mock_config_disabled)
        assert email.enabled is False
    
    def test_validate_attachment_size_success(self, mock_config_enabled, tmp_path):
        email = EmailManager(mock_config_enabled)
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("x" * 1024)  # 1KB
        
        assert email.validate_attachment_size(test_file) is True
    
    def test_validate_attachment_missing(self, mock_config_enabled, tmp_path):
        email = EmailManager(mock_config_enabled)
        
        missing = tmp_path / "missing.txt"
        
        with pytest.raises(PipelineError, match="Attachment not found"):
            email.validate_attachment_size(missing)
    
    def test_validate_attachment_too_large(self, mock_config_enabled, tmp_path):
        email = EmailManager(mock_config_enabled)
        
        large_file = tmp_path / "large.txt"
        large_file.write_bytes(b"x" * (15 * 1024 * 1024))  # 15MB
        
        with pytest.raises(PipelineError, match="exceeds limit"):
            email.validate_attachment_size(large_file)

    def test_send_email_disabled(self, mock_config_disabled):
        email = EmailManager(mock_config_disabled)
        result = email._send_email("Test", "<p>Test</p>", ["test@test.com"])
        assert result is False
    
    @patch('src.core.email.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp, mock_config_enabled):
        from unittest.mock import patch
        
        email = EmailManager(mock_config_enabled)
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = email._send_email("Test Subject", "<p>Body</p>", ["test@test.com"])
        
        assert result is True
        mock_server.login.assert_called_once_with('test@test.com', 'password')
        mock_server.send_message.assert_called_once()