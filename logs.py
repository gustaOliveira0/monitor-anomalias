import datetime
import time
import random

# Esse arquivo é responsavel por gerar os fake logs para testar o monitoramente, cada função gera um tipo diferente de log 
# que será analizado pelo arquivo analyzer e gerar um json com as informações pertinentes

def generate_logs(filename="logs.txt"):
    while True:
        generate_error_spike(filename)
        generate_brute_force_attempts(filename)
        generate_unauthorized_access(filename)
        time.sleep(10)

def generate_error_spike(filename):
    with open(filename, 'a') as f:
        now = datetime.datetime.now().replace(microsecond=0)
        for i in range(6):
            log_time = now + datetime.timedelta(seconds=i)
            entry = f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} ERROR Unexpected exception in authentication module {i+1}"
            f.write(entry + "\n")
            f.flush()

def generate_brute_force_attempts(filename):
    with open(filename, 'a') as f:
        now = datetime.datetime.now().replace(microsecond=0)
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
        for i in range(6):
            user_id = random.randint(1000, 9999)
            entry = f"{timestamp_str} INFO User login failed for user:user{user_id}"
            f.write(entry + "\n")
            f.flush()

def generate_unauthorized_access(filename):
    with open(filename, 'a') as f:
        now = datetime.datetime.now().replace(microsecond=0)
        entry1 = f"{now.strftime('%Y-%m-%d %H:%M:%S')} WARNING Unknown User attempted login"
        entry2 = f"{(now + datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')} WARNING Unauthorized access from IP:192.168.0.{random.randint(1,255)}"
        f.write(entry1 + "\n")
        f.write(entry2 + "\n")
        f.flush()

if __name__ == '__main__':
    generate_logs()
