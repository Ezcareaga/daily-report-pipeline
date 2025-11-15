import sys
sys.path.append('.')
import pytest
from src.core.exceptions import PipelineError, DatabaseError, ConfigurationError


class TestExceptions:
    
    def test_pipeline_error_inheritance(self):
        assert issubclass(DatabaseError, PipelineError)
        assert issubclass(ConfigurationError, PipelineError)
    
    def test_raise_database_error(self):
        with pytest.raises(DatabaseError):
            raise DatabaseError("Test error")
    
    def test_error_message(self):
        try:
            raise ConfigurationError("Config missing")
        except ConfigurationError as e:
            assert str(e) == "Config missing"