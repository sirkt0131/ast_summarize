import threading
import datetime

class ThreadSafeLogger:
    _instance = None
    _lock = threading.Lock()
    _file_path = 'log.txt'
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSafeLogger, cls).__new__(cls)
                cls._instance.file_path = cls._file_path
        return cls._instance

    def log(self, model, filename, input_token, input_cost, output_token, output_cost, total_cost):
        with self._lock:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}]\t{model}\t{filename}\t{input_token}\t{input_cost}\t{output_token}\t{output_cost}\t{total_cost}\n"
            with open(self.file_path, "a") as log_file:
                log_file.write(log_message)
