# Python Multithreading for Network API Operations

Multithreading is a technique used to execute multiple threads (smaller units of a process) concurrently. In Python, multithreading is particularly effective for **I/O-bound tasks**—such as fetching data from REST APIs, pinging network devices, or querying network management controllers.

---

## Why Use Multithreading for Network Tasks?

Network automation tasks are heavily **I/O-bound**. When a script sends an HTTP request to a switch or firewall, the CPU spends 99% of its time waiting for the remote host to respond across the network. 

* **Sequential Execution (Slow):** If 10 requests each take 2 seconds, sequential processing takes **20 seconds**.
* **Multithreaded Execution (Fast):** Running 10 requests concurrently across 10 threads reduces total time to **~2 seconds**.

> **Note on GIL (Global Interpreter Lock):** Python’s GIL prevents multiple threads from executing Python bytecodes simultaneously on multiple CPU cores (limiting CPU-bound performance). However, during I/O operations (like `requests.get()`), Python releases the GIL, making multithreading ideal for network operations.

---

## Key Concepts

* **Thread:** A lightweight, independent sequence of execution.
* **Worker:** A thread designated to execute a specific target function.
* **Thread Pool (`ThreadPoolExecutor`):** A managed collection of worker threads that reuse existing threads to execute tasks from a queue, avoiding thread creation overhead.

---

## 1. Basic Example: Standard Threading vs ThreadPoolExecutor

### A. Simple Threading (`threading.Thread`)
```python
import threading
import time

def task(name):
    print(f"Task {name} starting...")
    time.sleep(1)  # Simulates I/O delay
    print(f"Task {name} completed.")

# Creating individual threads
threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(f"T{i}",))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("All tasks finished.")

# Other Example for Network
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Target enterprise network devices
DEVICES = [
    {"name": "fw01", "ip": "10.10.10.1"},
    {"name": "fw02", "ip": "10.10.10.2"},
    {"name": "sw01", "ip": "10.20.10.1"},
    {"name": "sw02", "ip": "10.20.10.2"},
]

def fetch_device_status(device):
    """Worker function sending an HTTP GET request to a network host."""
    name = device["name"]
    ip = device["ip"]
    url = f"https://{ip}/api/v1/system/status"
    
    try:
        # Simulate API request with a 2-second network timeout
        response = requests.get(url, timeout=2, verify=False)
        return f"[{name}] Success - Status Code: {response.status_code}"
    except requests.exceptions.RequestException:
        # Graceful error handling for offline/unreachable hosts
        return f"[{name}] Failed - Unreachable or Timeout"

def run_parallel_checks():
    start_time = time.time()
    
    # Initialize thread pool with 4 concurrent workers
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks to the pool
        future_to_device = {
            executor.submit(fetch_device_status, dev): dev for dev in DEVICES
        }
        
        # Collect results as threads complete
        for future in as_completed(future_to_device):
            result = future.result()
            print(result)
            
    elapsed_time = time.time() - start_time
    print(f"\nExecution completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    run_parallel_checks()
