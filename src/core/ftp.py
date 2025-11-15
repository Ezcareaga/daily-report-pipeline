#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FTP/SFTP file transfer management."""

import ftplib
from pathlib import Path
from typing import Optional

from .config import ConfigManager
from .exceptions import PipelineError


class FTPManager:
    """Handles FTP file transfers."""
    
    def __init__(self, config: ConfigManager):
        """
        Initialize FTP manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.enabled = config.getboolean('FTP', 'habilitado', default=False)
        
        if self.enabled:
            self.host = config.get('FTP', 'servidor')
            self.port = config.getint('FTP', 'puerto', default=21)
            self.user = config.get('FTP', 'usuario')
            self.password = config.get('FTP', 'password', default='')
            self.remote_dir = config.get('FTP', 'directorio_remoto', default='/')
            self.use_passive = config.getboolean('FTP', 'modo_pasivo', default=True)
            
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish FTP connection.
        
        Returns:
            bool: True if connected
            
        Raises:
            PipelineError: If connection fails
        """
        if not self.enabled:
            return False
        
        try:
            self.connection = ftplib.FTP()
            self.connection.connect(self.host, self.port)
            self.connection.login(self.user, self.password)
            
            if self.use_passive:
                self.connection.set_pasv(True)
            
            if self.remote_dir and self.remote_dir != '/':
                self.connection.cwd(self.remote_dir)
            
            return True
            
        except ftplib.all_errors as e:
            raise PipelineError(f"FTP connection failed: {e}") from e
    
    def disconnect(self) -> None:
        """Close FTP connection safely."""
        if self.connection:
            try:
                self.connection.quit()
            except:
                self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()