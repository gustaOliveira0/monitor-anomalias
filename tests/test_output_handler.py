
import os
import json
from output_handler import save_anomaly

ANOMALY_FILE = "anomalies.json"

def clear_anomalies():
    if os.path.exists(ANOMALY_FILE):
        with open(ANOMALY_FILE, "w") as f:
            json.dump([], f)

def read_anomalies():
    if not os.path.exists(ANOMALY_FILE):
        return []
    with open(ANOMALY_FILE, "r") as f:
        return json.load(f)

def test_save_single_anomaly():
    clear_anomalies()
    anomaly = {
        "timestamp": "2025-04-18T12:00:00",
        "type": "error_spike",
        "message": "Detected 6 ERROR entries in 60 seconds"
    }
    save_anomaly(anomaly)
    data = read_anomalies()
    assert len(data) == 1
    assert data[0]["type"] == "error_spike"

def test_save_multiple_sorted_anomalies():
    clear_anomalies()
    anomalies = [
        {
            "timestamp": "2025-04-18T12:01:00",
            "type": "error_spike",
            "message": "Another error"
        },
        {
            "timestamp": "2025-04-18T12:00:00",
            "type": "brute_force",
            "message": "Detected brute force"
        }
    ]
    for anomaly in anomalies:
        save_anomaly(anomaly)
    data = read_anomalies()
    assert len(data) == 2
    assert data[0]["timestamp"] < data[1]["timestamp"]

def test_handles_empty_file_gracefully():
    with open(ANOMALY_FILE, "w") as f:
        f.write("")
    anomaly = {
        "timestamp": "2025-04-18T12:00:00",
        "type": "error_spike",
        "message": "Handled empty file"
    }
    save_anomaly(anomaly)
    data = read_anomalies()
    assert any(a["message"] == "Handled empty file" for a in data)