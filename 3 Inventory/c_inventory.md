Here is the complete C_inventory.md file documentation structured around your specific CSV formats, separate vendor inventories, and audit logging schemas.
# Device Inventory & Execution Logging Standards

This document defines the structured CSV schemas used by **Automo** to target enterprise network devices (firewalls, routers, and switches) across different vendors, as well as the standard logging schema generated after automation runs.

---

## Directory Structure

All target inventory files and log output must follow a predictable directory layout inside the repository:

```text
Automo/
├── inventory/
│   ├── inventory_fortigate_fw.csv
│   ├── inventory_fortigate_nw.csv
│   ├── inventory_cisco_fw.csv
│   ├── inventory_cisco_nw.csv
│   ├── inventory_paloalto_fw.csv
│   └── inventory_paloalto_nw.csv
└── logs/
    └── logfile.csv

CSV Naming Conventions & Schema
Inventory files are grouped by vendor (fortigate, cisco, paloalto) and device category:
 * *_fw.csv: Dedicated to security appliances (Firewalls).
 * *_nw.csv: Dedicated to network infrastructure (Routers and Switches).
Standard Inventory CSV Headers
All inventory files share the exact same 4-column structure:
hostname,domain,ipv4,ipv6

Example Inventory Files
1. Fortinet (FortiGate)
Firewalls (inventory_fortigate_fw.csv)
hostname,domain,ipv4,ipv6
fw01,company.com,10.10.10.1,2001:db8::1
fw02,company.com,10.10.10.2,2001:db8::2
fw03,company.com,10.10.10.3,2001:db8::3

Network Switches & Routers (inventory_fortigate_nw.csv)
hostname,domain,ipv4,ipv6
sw01,company.com,10.20.10.1,2001:db8:1::1
sw02,company.com,10.20.10.2,2001:db8:1::2

2. Cisco Systems
Firewalls (inventory_cisco_fw.csv)
hostname,domain,ipv4,ipv6
cisco-asa01,company.com,10.30.10.1,2001:db8:2::1
cisco-ftd01,company.com,10.30.10.2,2001:db8:2::2

Network Switches & Routers (inventory_cisco_nw.csv)
hostname,domain,ipv4,ipv6
cisco-core01,company.com,10.40.10.1,2001:db8:3::1
cisco-dist01,company.com,10.40.10.2,2001:db8:3::2

3. Palo Alto Networks
Firewalls (inventory_paloalto_fw.csv)
hostname,domain,ipv4,ipv6
pa-fw01,company.com,10.50.10.1,2001:db8:4::1
pa-fw02,company.com,10.50.10.2,2001:db8:4::2

Log File Format
Whenever an Automo automation script executes against target inventories, the execution output must append status reports to logs/logfile.csv.
Log CSV Headers
timestamp,hostname,ip,http,code,description

Log File Example (logfile.csv)
timestamp,hostname,ip,http,code,description
2026-09-02 10:00:00,fw01,10.10.10.1,GET,200,Success
2026-09-02 10:01:00,fw02,10.10.10.2,GET,401,Unauthorized
2026-09-02 10:02:00,fw03,10.10.10.3,POST,500,Server Error

Python Integration Example
Below is a snippet showing how Automo parses an inventory CSV file and appends execution status directly into the central log file:
import csv
from datetime import datetime
import requests

def run_automation_and_log(inventory_file, log_file):
    with open(inventory_file, mode='r') as inv_file:
        reader = csv.DictReader(inv_file)
        
        for row in reader:
            hostname = row['hostname']
            ip = row['ipv4']
            url = f"https://{ip}/api/v1/status"
            
            # Executing API call
            try:
                response = requests.get(url, timeout=5, verify=False)
                status_code = response.status_code
                description = "Success" if status_code == 200 else "Failed"
            except requests.exceptions.RequestException as e:
                status_code = 500
                description = "Connection Timeout/Error"

            # Writing to Log File
            log_entry = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                hostname,
                ip,
                "GET",
                status_code,
                description
            ]
            
            with open(log_file, mode='a', newline='') as l_file:
                writer = csv.writer(l_file)
                writer.writerow(log_entry)

# Example Execution
run_automation_and_log('inventory/inventory_fortigate_fw.csv', 'logs/logfile.csv')



