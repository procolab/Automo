import csv
import socket
from datetime import datetime
import requests

INVENTORY_FILE = 'inventory_web_srvr.csv'
LOG_FILE = 'logfile.csv'

def resolve_ip(domain):
    """Resolve FQDN domain to IPv4 address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "DNS_Resolution_Failed"

def run_owl_check():
    """Check each inventory domain and log response details."""
    with open(INVENTORY_FILE, mode='r') as inv_file:
        reader = csv.DictReader(inv_file)
        
        for row in reader:
            hostname = row['hostname']
            domain = row['domain']
            ip = resolve_ip(domain)
            
            # Default fallback values
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

            # Create log entry
            log_entry = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                hostname,
                ip,
                http_method,
                status_code,
                description
            ]

            # Append results to logfile.csv
            with open(LOG_FILE, mode='a', newline='') as log_f:
                writer = csv.writer(log_f)
                writer.writerow(log_entry)

            print(f"[{log_entry[0]}] Checked {hostname} ({domain}) -> Status: {status_code}")

if __name__ == "__main__":
    run_owl_check()
