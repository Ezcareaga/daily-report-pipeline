import sys
sys.path.append('.')
import pytest
from unittest.mock import Mock, patch
from src.core.database import DatabaseManager
from src.core.exceptions import DatabaseError


class TestDatabaseManager:
    
    @pytest.fixture
    def mock_config(self):
        config = Mock()
        config.get.side_effect = lambda section, key: {
            ('DATABASE', 'host'): 'localhost',
            ('DATABASE', 'service_name'): 'ORCL',
            ('DATABASE', 'user'): 'test',
            ('DATABASE', 'password'): 'pass'
        }.get((section, key))
        config.getint.return_value = 1521
        return config
    
    @patch('src.core.database.oracledb')
    def test_connect_success(self, mock_oracle, mock_config):
        db = DatabaseManager(mock_config)
        mock_oracle.connect.return_value = Mock()
        
        assert db.connect() is True
        mock_oracle.connect.assert_called_once()
    
    @patch('src.core.database.oracledb')
    def test_connect_failure(self, mock_oracle, mock_config):
        db = DatabaseManager(mock_config)
        mock_oracle.connect.side_effect = Exception("Connection failed")
        
        with pytest.raises(DatabaseError):
            db.connect()
    
    def test_execute_query_not_connected(self, mock_config):
        db = DatabaseManager(mock_config)
        
        with pytest.raises(DatabaseError, match="Not connected"):
            db.execute_query("SELECT 1")