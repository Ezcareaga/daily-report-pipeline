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