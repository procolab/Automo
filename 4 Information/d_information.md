Here is the complete d_information.md file covering both foundational and advanced patterns for working with JSON and CSV data structures in Python.
# Python JSON & CSV Data Handling Reference Guide

This document serves as a comprehensive guide for handling JSON (JavaScript Object Notation) and CSV (Comma-Separated Values) data structures using Python, ranging from primitive data mapping to advanced streaming and structured API operations.

---

## Part 1: JSON Handling in Python

Python provides the built-in `json` module to parse, serialize, and manipulate JSON data structures natively.

### 1. JSON Data Types vs. Python Native Types

| JSON Type | Python Equivalent | Example JSON | Example Python |
| :--- | :--- | :--- | :--- |
| **Object** | `dict` | `{"key": "val"}` | `{"key": "val"}` |
| **Array** | `list` | `["apple", "banana"]` | `["apple", "banana"]` |
| **String** | `str` | `"hello"` | `'hello'` |
| **Number (Int)** | `int` | `42` | `42` |
| **Number (Real)**| `float` | `3.14` | `3.14` |
| **Boolean** | `bool` | `true` / `false` | `True` / `False` |
| **Null** | `NoneType` | `null` | `None` |

---

### 2. Basic JSON Operations

#### **A. Strings to Python (`json.loads`) & Python to Strings (`json.dumps`)**

```python
import json

# JSON String -> Python Dictionary (Parsing / Deserialization)
json_string = '{"hostname": "fw01", "ports": [22, 443], "active": true, "location": null}'
data_dict = json.loads(json_string)

print(type(data_dict))       # <class 'dict'>
print(data_dict["active"])   # True (converted to Python bool)

# Python Dictionary -> JSON String (Serialization)
python_dict = {
    "device": "switch-01",
    "managed": True,
    "vlans": [10, 20, 30]
}
json_output = json.dumps(python_dict, indent=4)
print(json_output)

B. Direct File Operations (json.load and json.dump)
import json

# Writing Python dict directly to a .json file
data = {"config_version": 1.2, "status": "enabled"}

with open("config.json", mode="w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

# Reading directly from a .json file into a Python dict
with open("config.json", mode="r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print(loaded_data["config_version"])  # Output: 1.2

3. Advanced JSON Operations
A. Custom Class Serialization using json.JSONEncoder
By default, Python's json module cannot serialize complex custom objects (e.g., datetime, sets, custom classes).
import json
from datetime import datetime

class CustomDevice:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.last_checked = datetime.now()

class DeviceEncoder(json.JSONEncoder):
    """Custom serializer for non-standard Python objects."""
    def default(self, obj):
        if isinstance(obj, CustomDevice):
            return {
                "name": obj.name,
                "ip": obj.ip,
                "last_checked": obj.last_checked.isoformat()
            }
        return super().default(obj)

# Usage
device = CustomDevice("core-router-01", "192.168.1.1")
encoded_json = json.dumps(device, cls=DeviceEncoder, indent=2)
print(encoded_json)

B. Flattening Nested JSON Payloads
Network API responses often contain complex, multi-level nested dictionaries. You can recursively flatten them into simple key-value pairs:
def flatten_json(nested_json, parent_key='', sep='.'):
    """Recursively flattens deeply nested JSON structures."""
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Nested API Response
api_data = {
    "device": {
        "identity": {"hostname": "border-fw", "site": "HQ"},
        "interfaces": {"eth0": "10.0.0.1"}
    }
}

flat_data = flatten_json(api_data)
print(flat_data)
# Output: {'device.identity.hostname': 'border-fw', 'device.identity.site': 'HQ', 'device.interfaces.eth0': '10.0.0.1'}

Part 2: CSV File Handling in Python
Python’s standard library includes the csv module for structured tabular data processing.
1. Basic CSV Reader & Writer
import csv

# Writing simple rows to CSV
with open("devices.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["hostname", "ip", "status"])  # Header row
    writer.writerow(["fw01", "10.0.0.1", "active"])
    writer.writerow(["sw01", "10.0.0.2", "inactive"])

# Reading simple rows from CSV
with open("devices.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # Output: list of strings

2. Dictionary-Based CSV Operations (DictReader & DictWriter)
DictReader and DictWriter map row data directly into Python dictionaries using header keys, preventing positional indexing errors.
import csv

# Writing dictionaries to CSV
fieldnames = ["hostname", "ip", "vlan"]
data_rows = [
    {"hostname": "router-01", "ip": "172.16.0.1", "vlan": 10},
    {"hostname": "router-02", "ip": "172.16.0.2", "vlan": 20}
]

with open("inventory.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_rows)

# Reading CSV as dictionaries
with open("inventory.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"Host: {row['hostname']} | IP: {row['ip']} | VLAN: {row['vlan']}")

3. Advanced CSV & JSON Interoperability
Converting a JSON API Response directly to a CSV File
import csv
import json

json_data = '''
[
    {"timestamp": "2026-09-02 10:00:00", "hostname": "fw01", "ip": "10.10.10.1", "code": 200},
    {"timestamp": "2026-09-02 10:01:00", "hostname": "fw02", "ip": "10.10.10.2", "code": 401}
]
'''

records = json.loads(json_data)

# Dynamically extract headers from the first JSON object
headers = list(records[0].keys())

with open("api_export.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(records)

print("JSON successfully mapped and exported to api_export.csv")


