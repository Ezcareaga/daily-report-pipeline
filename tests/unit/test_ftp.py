#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for FTPManager."""

import sys
sys.path.append('.')
import pytest
from unittest.mock import Mock, patch

from src.core.ftp import FTPManager
from src.core.exceptions import PipelineError


class TestFTPManager:
    
    @pytest.fixture
    def mock_config_enabled(self):
        config = Mock()
        config.getboolean.side_effect = lambda section, key, default=False: {
            ('FTP', 'habilitado'): True,
            ('FTP', 'modo_pasivo'): True
        }.get((section, key), default)
        
        config.get.side_effect = lambda section, key, default=None: {
            ('FTP', 'servidor'): 'ftp.test.com',
            ('FTP', 'usuario'): 'testuser',
            ('FTP', 'password'): 'testpass',
            ('FTP', 'directorio_remoto'): '/uploads'
        }.get((section, key), default)
        
        config.getint.return_value = 21
        return config
    
    @pytest.fixture
    def mock_config_disabled(self):
        config = Mock()
        config.getboolean.return_value = False
        return config
    
    def test_init_enabled(self, mock_config_enabled):
        ftp = FTPManager(mock_config_enabled)
        assert ftp.enabled is True
        assert ftp.host == 'ftp.test.com'
        assert ftp.port == 21
        assert ftp.user == 'testuser'
    
    def test_init_disabled(self, mock_config_disabled):
        ftp = FTPManager(mock_config_disabled)
        assert ftp.enabled is False
    
    def test_connect_disabled(self, mock_config_disabled):
        ftp = FTPManager(mock_config_disabled)
        assert ftp.connect() is False
    
    @patch('src.core.ftp.ftplib.FTP')
    def test_connect_success(self, mock_ftp_class, mock_config_enabled):
        ftp = FTPManager(mock_config_enabled)
        mock_conn = Mock()
        mock_ftp_class.return_value = mock_conn
        
        result = ftp.connect()
        
        assert result is True
        mock_conn.connect.assert_called_once_with('ftp.test.com', 21)
        mock_conn.login.assert_called_once_with('testuser', 'testpass')
        mock_conn.cwd.assert_called_once_with('/uploads')
    
    def test_disconnect(self, mock_config_enabled):
        ftp = FTPManager(mock_config_enabled)
        mock_conn = Mock()
        ftp.connection = mock_conn
        
        ftp.disconnect()
        
        mock_conn.quit.assert_called_once()
        assert ftp.connection is None

    @patch('src.core.ftp.ftplib.FTP')
    def test_upload_file_success(self, mock_ftp_class, mock_config_enabled, tmp_path):
        ftp = FTPManager(mock_config_enabled)
        mock_conn = Mock()
        mock_ftp_class.return_value = mock_conn
        ftp.connect()
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")
        
        result = ftp.upload_file(test_file)
        
        assert result is True
        mock_conn.storbinary.assert_called_once()
    
    def test_upload_file_not_connected(self, mock_config_enabled, tmp_path):
        ftp = FTPManager(mock_config_enabled)
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        with pytest.raises(PipelineError, match="Not connected"):
            ftp.upload_file(test_file)
    
    def test_upload_file_missing(self, mock_config_enabled, tmp_path):
        ftp = FTPManager(mock_config_enabled)
        ftp.connection = Mock()
        
        missing_file = tmp_path / "missing.txt"
        
        with pytest.raises(PipelineError, match="File not found"):
            ftp.upload_file(missing_file)

    def test_validate_file_success(self, mock_config_enabled, tmp_path):
        ftp = FTPManager(mock_config_enabled)
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("x" * 1024)
        
        assert ftp.validate_file(test_file, max_size_mb=1) is True
    
    def test_validate_file_too_large(self, mock_config_enabled, tmp_path):
        ftp = FTPManager(mock_config_enabled)
        
        large_file = tmp_path / "large.txt"
        large_file.write_bytes(b"x" * (2 * 1024 * 1024))
        
        with pytest.raises(PipelineError, match="exceeds limit"):
            ftp.validate_file(large_file, max_size_mb=1)