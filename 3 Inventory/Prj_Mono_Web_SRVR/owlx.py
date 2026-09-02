import csv
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

INVENTORY_FILE = 'inventory_web_srvr.csv'
LOG_FILE = 'logfile.csv'
MAX_THREADS = 10  # Number of parallel workers

def resolve_ip(domain):
    """Resolve FQDN domain to IPv4 address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "DNS_Resolution_Failed"

def check_host(row):
    """Worker function to check a single domain and build log entry."""
    hostname = row['hostname']
    domain = row['domain']
    ip = resolve_ip(domain)
    
    http_method = "GET"
    status_code = 500
    description = "Connection Failed"

    if ip != "DNS_Resolution_Failed":
        url = f"https://{domain}"
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            status_code = response.status_code
            description = response.reason
        except requests.exceptions.RequestException as e:
            status_code = 500
            description = type(e).__name__
    else:
        description = "Unable to resolve domain"

    log_entry = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        hostname,
        ip,
        http_method,
        status_code,
        description
    ]

    return log_entry

def run_owl_check():
    """Reads inventory, runs checks in parallel using multithreading, and logs results."""
    # 1. Read inventory into memory
    with open(INVENTORY_FILE, mode='r') as inv_file:
        reader = list(csv.DictReader(inv_file))

    log_entries = []

    # 2. Process hosts concurrently
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(check_host, row) for row in reader]
        
        for future in as_completed(futures):
            entry = future.result()
            log_entries.append(entry)
            print(f"[{entry[0]}] Checked {entry[1]} ({entry[2]}) -> Status: {entry[4]}")

    # 3. Append all results safely to logfile.csv
    with open(LOG_FILE, mode='a', newline='') as log_f:
        writer = csv.writer(log_f)
        writer.writerows(log_entries)

if __name__ == "__main__":
    run_owl_check()
  
