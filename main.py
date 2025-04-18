import threading
import logs
import analyzer

# Esse aquivo é simples ele simplesmente junta tudo, ele inicia as threads par todas os fake logs
# simultaneamente :)

def start():
    log_thread = threading.Thread(target=logs.generate_logs, args=("logs.txt",), daemon=True)
    analyzer_thread = threading.Thread(target=analyzer.watch_log_for_error_spikes, args=("logs.txt",))

    #Inicia as threads
    log_thread.start()
    analyzer_thread.start()
    
    #Mantem o programa princiapl até terminar
    analyzer_thread.join()

if __name__ == '__main__':
    start()
