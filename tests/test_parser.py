
from parser import parse_log_line
from datetime import datetime

def test_parse_valid_line():
    line = "2025-04-18 12:00:00 [ERROR] Something went wrong"
    result = parse_log_line(line)
    assert result is not None
    timestamp, level, message = result
    assert isinstance(timestamp, datetime)
    assert level == "ERROR"
    assert message == "Something went wrong"

def test_parse_invalid_format():
    line = "invalid line format"
    result = parse_log_line(line)
    assert result is None

def test_parse_valid_warning():
    line = "2025-04-18 14:15:30 [WARNING] Unknown user attempted login"
    result = parse_log_line(line)
    assert result is not None
    timestamp, level, message = result
    assert level == "WARNING"
    assert "Unknown user" in message

def test_parse_valid_info():
    line = "2025-04-18 14:15:30 [INFO] User login failed"
    result = parse_log_line(line)
    assert result is not None
    timestamp, level, message = result
    assert level == "INFO"
    assert "User login failed" in message

def test_parse_valid_debug():
    line = "2025-04-18 14:15:30 [DEBUG] Debugging mode enabled"
    result = parse_log_line(line)
    assert result is not None
    timestamp, level, message = result
    assert level == "DEBUG"
    assert "Debugging mode enabled" in message