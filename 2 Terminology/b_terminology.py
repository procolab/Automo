### 1. Validate "IPv4" and "IPv6"
import ipaddress
print('1. Validate "IPv4" and "IPv6"')
ip = "192.168.1.10"
obj = ipaddress.ip_address(ip)
print(obj.version)

ip = "2001:db8::1"
obj = ipaddress.ip_address(ip)
print(obj.version)

print('--------------------------------')

### 2. DNS Info "Domain to IP (Forward DNS Lookup)"
import socket
print('2. DNS Info "Domain to IP (Forward DNS Lookup)"')

domain = "google.com"
ip = socket.gethostbyname(domain)
print(ip)

print('--------------------------------')

### 3. Working with URLs
from urllib.parse import urlparse
print('3. Working with URLs')
# URL :       https://api.company.com/users?id=101
# Part :      Value
# Protocol :  https
# Hostname :  api.company.com
# Path :      /users
# Query :     id=101

url = "https://api.company.com/users?id=101"
parsed = urlparse(url)
print(parsed.scheme)
print(parsed.hostname)
print(parsed.path)
print(parsed.query)

print('--------------------------------')

### 4. Calling URL Using Requests
import requests
print('4. Calling URL Using Requests')

url = "https://www.google.com/"
response = requests.get(url) # HTTP Code

print(response.status_code)
# print(response.json()) # Uncomment if return date is JSON type

print('--------------------------------')

### 5. Inventory + API Automation
print('5. Inventory + API Automation')
inventory = [
    {
        "hostname": "router1",
        "ip": "10.1.1.1"
    },
    {
        "hostname": "router2",
        "ip": "10.1.1.2"
    }
]

for device in inventory:
    print(device["hostname"])
    print(device["ip"])

print('Real-world use: inventory info use in URL.')

for device in inventory:
    url = f"https://monitoring.company.com/device/{device['hostname']}"
    print(url)

print('--------------------------------')
