import pytest
from parser import parse_log_line
from datetime import datetime

def test_parse_valid_log_line():
    line = "2025-04-18 21:23:32 ERROR Unexpected exception in authentication module"
    result = parse_log_line(line)
    assert result is not None
    timestamp, level, message = result
    assert isinstance(timestamp, datetime)
    assert level == "ERROR"
    assert "Unexpected exception" in message

def test_parse_invalid_log_line():
    line = "Invalid log format"
    result = parse_log_line(line)
    assert result is None
