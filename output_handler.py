import json
import os

ANOMALY_FILE = "anomalies.json"

def save_anomaly(anomaly):
    if not os.path.exists(ANOMALY_FILE):
        with open(ANOMALY_FILE, "w") as f:
            json.dump([], f, indent=2)

    with open(ANOMALY_FILE, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(anomaly)
        data.sort(key=lambda x: x['timestamp'])

        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)
