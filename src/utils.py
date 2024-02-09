import re
from src.cost import Cost
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_text(text):
    text = text.replace('-\n', '')
    text = re.sub(r'\s+', ' ', text)
    return text


def split_text(text, wc_max):
    words = text.split()
    chunks = [' '.join(words[i:i + wc_max])
              for i in range(0, len(words), wc_max)]
    return chunks

def sum_cost(costs):
    total = Cost(0,0,0,0)
    for c in costs:
        total.input_token += c.input_token
        total.input_cost += c.input_cost
        total.output_token += c.output_token
        total.output_cost += c.output_cost
        total.total_cost += c.total_cost
    return total

class RateLimiter:
    def __init__(self, calls_per_minute, max_workers):
        self.interval = 60.0 / calls_per_minute
        self.lock = threading.Lock()
        self.last_call = time.time() - self.interval
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            with self.lock:
                current_time = time.time()
                elapsed = current_time - self.last_call
                wait_time = max(0, self.interval - elapsed)
                if wait_time > 0:
                    time.sleep(wait_time)
                self.last_call = time.time()
            return func(*args, **kwargs)
        return wrapped