import json
import os

#apenas mantem o arquvio de anomalias atualizado, nada muito grandioso aqui

ANOMALY_FILE = "anomalies.json"

def save_anomaly(anomaly):
    try:
        if not os.path.exists(ANOMALY_FILE):
            with open(ANOMALY_FILE, 'w') as f:
                json.dump([], f)

        with open(ANOMALY_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            data.append(anomaly)
            data.sort(key=lambda x: x['timestamp'])  # garante ordem
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
        print("[Arquivo salvo] anomalies.json atualizado", flush=True)
    except Exception as e:
        print("[Erro ao salvar anomalia]", str(e), flush=True)
