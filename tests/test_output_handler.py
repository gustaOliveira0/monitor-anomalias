import os
import json
import pytest
from output_handler import save_anomaly, ANOMALY_FILE

def setup_function():
    if os.path.exists(ANOMALY_FILE):
        os.remove(ANOMALY_FILE)

def test_save_anomaly_creates_file():
    anomaly = {
        "timestamp": "2025-04-18T21:23:32",
        "type": "error_spike",
        "message": "Detected 6 ERROR entries in 60 seconds"
    }
    save_anomaly(anomaly)
    assert os.path.exists(ANOMALY_FILE)

    with open(ANOMALY_FILE) as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert anomaly in data

def test_save_anomaly_orders_by_timestamp():
    anomaly1 = {
        "timestamp": "2025-04-18T21:23:32",
        "type": "error_spike",
        "message": "Detected 6 ERROR entries in 60 seconds"
    }
    anomaly2 = {
        "timestamp": "2025-04-18T21:22:32",
        "type": "brute_force",
        "message": "Detected 6 login attempts in the same second"
    }

    save_anomaly(anomaly1)
    save_anomaly(anomaly2)

    with open(ANOMALY_FILE) as f:
        data = json.load(f)
        assert data[0]["timestamp"] == anomaly2["timestamp"]
        assert data[1]["timestamp"] == anomaly1["timestamp"]
