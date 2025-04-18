from datetime import datetime, timedelta
from collections import deque, defaultdict
import time
from parser import parse_log_line
from output_handler import save_anomaly


#Arquivo responsavel por monitoriar o arquivos dos fakelogs (logs.txt) e capturar as anomalias de acordo com sua natureza

LOG_FILE = "logs.txt"

def watch_log_for_error_spikes(log_path, test_mode=False):
    error_window = deque()
    seen_lines = set()
    login_counts = defaultdict(int)

    while True:
        try:
            with open(log_path, 'r') as file:
                lines = file.readlines()

            new_lines = [line for line in lines if line not in seen_lines]
            seen_lines.update(new_lines)

            for line in new_lines:
                parsed = parse_log_line(line)
                if not parsed:
                    continue

                timestamp, level, message = parsed

                # Spike de erro
                if level == "ERROR":
                    error_window.append(timestamp)
                    while error_window and (timestamp - error_window[0]) > timedelta(seconds=60):
                        error_window.popleft()

                    if len(error_window) >= 6:
                        anomaly = {
                            "timestamp": timestamp.isoformat(),
                            "type": "error_spike",
                            "message": f"Detected {len(error_window)} ERROR entries in 60 seconds"
                        }
                        print("[Anomalia detectada]", anomaly, flush=True)
                        save_anomaly(anomaly)
                        error_window.clear()

                # Força bruta
                if level == "INFO" and "User login failed" in message:
                    second_key = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    login_counts[second_key] += 1

                    if login_counts[second_key] == 6:
                        anomaly = {
                            "timestamp": timestamp.isoformat(),
                            "type": "brute_force",
                            "message": f"Detected {login_counts[second_key]} login attempts in the same second"
                        }
                        print("[Anomalia detectada]", anomaly, flush=True)
                        save_anomaly(anomaly)

                # Acesso não autorizado
                if "Unknown User" in message or "Unauthorized access" in message:
                    anomaly = {
                        "timestamp": timestamp.isoformat(),
                        "type": "unauthorized_access",
                        "message": message
                    }
                    print("[Anomalia detectada]", anomaly, flush=True)
                    save_anomaly(anomaly)

            if test_mode:
                return  # encerra imediatamente sem delay

            time.sleep(1)

        except KeyboardInterrupt:
            print("\n[Analyzer] Encerrando monitoramento.", flush=True)
            break
        except Exception as e:
            print("[Erro no monitoramento]", str(e), flush=True)
            if test_mode:
                return  # não dorme no erro quando for teste
            time.sleep(2)

if __name__ == '__main__':
    watch_log_for_error_spikes(LOG_FILE)
