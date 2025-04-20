from datetime import datetime, timedelta
from parser import parse_log_line
from output_handler import save_anomaly

def analyze_log_file(log_path: str):
    # Lê e faz o parse dos logs
    with open(log_path, "r") as f:
        lines = f.readlines()

    parsed_logs = [parse_log_line(line) for line in lines]
    parsed_logs = [log for log in parsed_logs if log is not None]

    saved_error_windows = set()
    saved_brute_force = set()
    saved_unauthorized = set()

    total_logs = len(parsed_logs)
    i = 0

    while i < total_logs:
        timestamp, level, message = parsed_logs[i]

        if "unknown user" in message.lower() or "unauthorized access" in message.lower():
            key = (timestamp.isoformat(), message.lower())
            if key not in saved_unauthorized:
                save_anomaly({
                    "timestamp": timestamp.isoformat(),
                    "type": "unauthorized_access",
                    "message": message
                })
                saved_unauthorized.add(key)

        if level == "ERROR":
            start_time = timestamp
            end_time = start_time + timedelta(seconds=60)
            count = 1
            j = i + 1

            while j < total_logs:
                ts_j, lvl_j, _ = parsed_logs[j]
                if ts_j > end_time:
                    break
                if lvl_j == "ERROR":
                    count += 1
                j += 1

            if count > 5:
                key = start_time.isoformat()
                if key not in saved_error_windows:
                    save_anomaly({
                        "timestamp": start_time.isoformat(),
                        "type": "error_spike",
                        "message": f"Detected {count} ERROR entries in 60 seconds (from {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')})"
                    })
                    saved_error_windows.add(key)

            i = j
            continue

        i += 1

    login_logs = [log for log in parsed_logs if log[1] == "INFO" and "user login" in log[2].lower()]

    for i in range(len(login_logs)):
        t0 = login_logs[i][0]
        count = 1
        j = i + 1

        while j < len(login_logs) and login_logs[j][0] <= t0 + timedelta(seconds=1):
            count += 1
            j += 1

        key = ("brute_force", t0.isoformat())
        if count > 5 and key not in saved_brute_force:
            save_anomaly({
                "timestamp": t0.isoformat(),
                "type": "brute_force",
                "message": f"Detected {count} login attempts in 1 second (from {t0.strftime('%H:%M:%S')} to {(t0 + timedelta(seconds=1)).strftime('%H:%M:%S')})"
            })
            saved_brute_force.add(key)

