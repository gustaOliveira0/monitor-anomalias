
import os
import json
from datetime import datetime
from anomalies_analyzer import analyze_log_file

TEST_LOG_FILE = "test_logs.log"
ANOMALIES_FILE = "anomalies.json"

def write_logs(logs):
    with open(TEST_LOG_FILE, "w") as f:
        f.write("\n".join(logs))

def read_anomalies():
    if not os.path.exists(ANOMALIES_FILE):
        return []
    with open(ANOMALIES_FILE, "r") as f:
        return json.load(f)

def clear_anomalies():
    with open(ANOMALIES_FILE, "w") as f:
        json.dump([], f)

def test_detects_error_spike():
    clear_anomalies()
    logs = [
        "2025-04-18 12:00:00 [ERROR] Something went wrong",
        "2025-04-18 12:00:10 [ERROR] Something went wrong",
        "2025-04-18 12:00:20 [ERROR] Something went wrong",
        "2025-04-18 12:00:30 [ERROR] Something went wrong",
        "2025-04-18 12:00:40 [ERROR] Something went wrong",
        "2025-04-18 12:00:50 [ERROR] Something went wrong"
    ]
    write_logs(logs)
    analyze_log_file(TEST_LOG_FILE)
    anomalies = read_anomalies()
    assert any(a["type"] == "error_spike" for a in anomalies)

def test_does_not_detect_error_spike_below_threshold():
    clear_anomalies()
    logs = [
        "2025-04-18 13:00:00 [ERROR] Something went wrong",
        "2025-04-18 13:00:20 [ERROR] Something went wrong",
        "2025-04-18 13:00:40 [ERROR] Something went wrong"
    ]
    write_logs(logs)
    analyze_log_file(TEST_LOG_FILE)
    anomalies = read_anomalies()
    assert not any(a["type"] == "error_spike" for a in anomalies)

def test_detects_brute_force():
    clear_anomalies()
    logs = [
        "2025-04-18 14:00:00 [INFO] User login failed",
        "2025-04-18 14:00:00 [INFO] User login failed",
        "2025-04-18 14:00:00 [INFO] User login failed",
        "2025-04-18 14:00:00 [INFO] User login failed",
        "2025-04-18 14:00:00 [INFO] User login failed",
        "2025-04-18 14:00:00 [INFO] User login failed"
    ]
    write_logs(logs)
    analyze_log_file(TEST_LOG_FILE)
    anomalies = read_anomalies()
    assert any(a["type"] == "brute_force" for a in anomalies)

def test_detects_unauthorized_access():
    clear_anomalies()
    logs = [
        "2025-04-18 15:00:00 [WARNING] Unknown user attempted login",
        "2025-04-18 15:00:01 [WARNING] Unauthorized access from IP"
    ]
    write_logs(logs)
    analyze_log_file(TEST_LOG_FILE)
    anomalies = read_anomalies()
    types = {a["type"] for a in anomalies}
    assert "unauthorized_access" in types

def test_ignores_non_anomalous_logs():
    clear_anomalies()
    logs = [
        "2025-04-18 16:00:00 [INFO] User logged in",
        "2025-04-18 16:01:00 [INFO] Action successful"
    ]
    write_logs(logs)
    analyze_log_file(TEST_LOG_FILE)
    anomalies = read_anomalies()
    assert anomalies == []