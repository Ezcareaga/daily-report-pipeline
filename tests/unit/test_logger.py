import sys
sys.path.append('.')
import pytest
from src.core.logger import LoggerSetup

def test_logger_setup():
    from loguru import logger
    LoggerSetup.configure(name="test", level="DEBUG")
    assert True