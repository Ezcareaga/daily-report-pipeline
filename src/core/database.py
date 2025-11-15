#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Database connection and query management."""

import oracledb 
from pathlib import Path 
from typng import Optional, List, Tuple, Any
from datetime import datetime 

from .config import ConfigManager 
from .exceptions import DataBaseError

class DatabaseManager:
    """Handles all database operations"""

    def __init__(self, config: ConfigManager):
        """"
        Initialize database manager.

        Args:
            Config: ConfigManager instance with DB credentials
        """
        self.config = config
        self.connection = None
        self.cursor = None

        self.host = config.get('DATABASE', 'host')
        self.port = config.getint('DATABASE', 'port')
        self.service = config.get('DATABASE', 'service_name')
        self.user = config.get('DATABASE', 'user')
        self.password = config.get('DATABASE', 'password')

    def connect(self) -> bool:
        """
        Establish database connection.

        Returns:
            bool: True if connection succesuful
        
        Raises:
            DatabaseError: If connection fails
        """
        try: 
            dsn = oracledb.makedsn(
                self.host,
                self.port,
                service_name=self.service
            )

            self.connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=dsn
            )

            self.cursor = self.connection.cursor()

            return True

        except oracledb.Error as e: 
            error_msg = f"Database connection failed: {e}"
            raise DatabaseError(error_msg)

    def disconnect(self):
        """Close database connection safely"""
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_quuery(self, query: str, params: Optional[dict] = None) -> List[Tuple]:
        """
        Execute SELECT query and return results.

        Args: 
            query: SQL query string
            params: Dictionary of parameters for query

        Returns:
            List of tuples with query results

        Raises:
            DatabaseError: If query fails
        """
        if not self.connection:
            raise DatabaseError("Not connected to database")

        try:
            if params: 
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            return self.cursor.fetchall()

        except oracledb.Error as e:
            raise DatabaseError(f"Query failed: {e}")

    def check_data_exists(self, date: datetime) -> Tuple[bool, int]:
        """
        Check if data exists for given date.

        Args:
            date: Date to check

        Returns: 
            Tuple of (exits: bool, count: int)
        """
        query = """"
            SELECT COUNT(*)
            FROM transactions
            WHERE TRUNC(transaction_date) = TRUNC(:check_date)
        """

        try: 
            self.cursor.execute(query, {'check_date': date})
            count = self.cursor.fetchone()[0] 
            return(count > 0, count)

        except oracledb.Error as e:
            raise DatabaseError(f"Error checking data: {e}")

    def __enter__(self):
        """Context manager entry - allows 'with DatabaseManager() as db:'"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed"""
        self.disconnect()