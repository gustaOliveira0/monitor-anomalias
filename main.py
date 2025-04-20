from anomalies_analyzer import analyze_log_file

if __name__ == '__main__':
    LOG_FILE = "app_anomalies.log"  # substitua pelo nome do arquivo real, se necessário
    print("[Main] Iniciando análise do arquivo de log...")
    analyze_log_file(LOG_FILE)
    print("[Main] Análise concluída. Resultados salvos em anomalies.json")
