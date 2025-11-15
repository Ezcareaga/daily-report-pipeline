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

    def upload_file(self, local_path: Path, remote_filename: Optional[str] = None) -> bool:
        """
        Upload file to FTP server.
        
        Args:
            local_path: Path to local file
            remote_filename: Optional remote filename (uses local name if None)
            
        Returns:
            bool: True if uploaded successfully
            
        Raises:
            PipelineError: If upload fails
        """
        if not self.enabled:
            return False
        
        local_path = Path(local_path)
        
        if not local_path.exists():
            raise PipelineError(f"File not found: {local_path}")
        
        if not self.connection:
            raise PipelineError("Not connected to FTP server")
        
        filename = remote_filename or local_path.name
        
        try:
            with open(local_path, 'rb') as f:
                self.connection.storbinary(f'STOR {filename}', f)
            return True
            
        except ftplib.all_errors as e:
            raise PipelineError(f"Upload failed: {e}") from e

    def validate_file(self, file_path: Path, max_size_mb: Optional[int] = None) -> bool:
        """
        Validate file before upload.
        
        Args:
            file_path: Path to file
            max_size_mb: Optional maximum file size in MB
            
        Returns:
            bool: True if valid
            
        Raises:
            PipelineError: If validation fails
        """
        if not file_path.exists():
            raise PipelineError(f"File not found: {file_path}")
        
        if max_size_mb:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                raise PipelineError(
                    f"File size ({size_mb:.2f}MB) exceeds limit ({max_size_mb}MB)"
                )
        
        return True