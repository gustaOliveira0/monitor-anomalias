import os
import json
import pytest
from analyzer import watch_log_for_error_spikes
from output_handler import ANOMALY_FILE

TEST_LOG_FILE = "logs_test.txt"

# Setup automático antes de cada teste
def setup_function():
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    if os.path.exists(ANOMALY_FILE):
        os.remove(ANOMALY_FILE)

# Utilitário para simular logs
def write_test_logs(lines):
    with open(TEST_LOG_FILE, 'a') as f:
        for line in lines:
            f.write(line + '\n')

# ✅ Testa detecção de spike de erro
def test_detects_error_spike():
    lines = [
        f"2025-04-18 21:00:0{i} ERROR Unexpected exception" for i in range(6)
    ]
    write_test_logs(lines)
    try:
        watch_log_for_error_spikes(TEST_LOG_FILE, test_mode=True)
    except SystemExit:
        pass

    with open(ANOMALY_FILE) as f:
        data = json.load(f)
        assert any(d["type"] == "error_spike" for d in data)

# ✅ Testa detecção de brute force
def test_detects_brute_force():
    lines = [
        f"2025-04-18 21:01:00 INFO User login failed for user:user{i}" for i in range(6)
    ]
    write_test_logs(lines)
    try:
        watch_log_for_error_spikes(TEST_LOG_FILE, test_mode=True)
    except SystemExit:
        pass

    with open(ANOMALY_FILE) as f:
        data = json.load(f)
        assert any(d["type"] == "brute_force" for d in data)

# ✅ Testa detecção de acesso não autorizado
def test_detects_unauthorized_access():
    lines = [
        "2025-04-18 21:02:00 WARNING Unknown User attempted login",
        "2025-04-18 21:02:01 WARNING Unauthorized access from IP:192.168.0.100"
    ]
    write_test_logs(lines)
    try:
        watch_log_for_error_spikes(TEST_LOG_FILE, test_mode=True)
    except SystemExit:
        pass

    with open(ANOMALY_FILE) as f:
        data = json.load(f)
        types = [d["type"] for d in data]
        assert types.count("unauthorized_access") == 2

# ✅ Testa que não dispara se não atingir o limite
def test_does_not_trigger_with_few_errors():
    lines = [
        f"2025-04-18 21:03:0{i} ERROR Something went wrong" for i in range(5)
    ]
    write_test_logs(lines)
    try:
        watch_log_for_error_spikes(TEST_LOG_FILE, test_mode=True)
    except SystemExit:
        pass

    assert not os.path.exists(ANOMALY_FILE)

# ✅ Testa log inválido (regex não casa)
def test_ignores_invalid_log_lines():
    lines = [
        "completely broken line",
        "2025-04-18 nonsense log entry",
        "invalid timestamp INFO something"
    ]
    write_test_logs(lines)
    try:
        watch_log_for_error_spikes(TEST_LOG_FILE, test_mode=True)
    except SystemExit:
        pass

    assert not os.path.exists(ANOMALY_FILE)

# ✅ Testa erro de leitura do arquivo (arquivo não existe)
def test_file_not_found_handling():
    try:
        watch_log_for_error_spikes("arquivo_inexistente.txt", test_mode=True)
    except SystemExit:
        pass
