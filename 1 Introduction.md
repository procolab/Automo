Here is the complete, expanded Introduction.md file updated to include a full HTTP Status Code reference guide and direct developer documentation links for major enterprise network vendors.
# Introduction to REST API & Network Automation

Welcome to **Automo**. This guide covers the foundational mechanics of REST APIs, compares raw terminal testing (`curl`) against programmatic automation (`Python requests`), breaks down standard HTTP status codes, and provides official API integration links for major enterprise network vendors.

---

## What is a REST API?

**Representational State Transfer (REST)** is an architectural style for designing networked applications over HTTP/HTTPS. REST APIs use standard HTTP verbs to perform **CRUD** (Create, Read, Update, Delete) operations on server resources:

| HTTP Method | CRUD Operation | Purpose | Payload Support |
| :--- | :--- | :--- | :--- |
| **`GET`** | **Read** | Retrieve resources without modifying system state | No payload |
| **`POST`** | **Create** | Create a new resource on the target host | JSON / Form / Text |
| **`PUT`** | **Update (Full)** | Completely replace an existing resource | JSON / Form / Text |
| **`PATCH`** | **Update (Partial)**| Modify specific attributes of an existing resource | JSON / Form / Text |
| **`DELETE`** | **Delete** | Remove a resource from the target host | Optional payload |

---

## HTTP Response Status Codes

HTTP status codes indicate whether a specific API request was successfully completed. Understanding these responses is critical for error handling in network automation scripts:

### 🟢 2xx Success (Request succeeded)
- **`200 OK`**: Request succeeded. Returned on successful `GET`, `PUT`, or `PATCH` requests.
- **`201 Created`**: Resource created successfully. Returned on successful `POST` requests.
- **`202 Accepted`**: Request accepted for processing, but processing is incomplete (common in asynchronous network deployments).
- **`204 No Content`**: Request succeeded, but there is no response body (common for `DELETE` operations).

### 🟡 3xx Redirection (Further action needed)
- **`301 Moved Permanently`**: Target URI has been moved permanently to a new location.
- **`302 Found`**: Temporary redirect to another URI.
- **`304 Not Modified`**: Resource has not changed since the last request (used for caching).

### 🔴 4xx Client Errors (Invalid request sent by client)
- **`400 Bad Request`**: Malformed request syntax, invalid parameters, or invalid JSON body.
- **`401 Unauthorized`**: Authentication is missing or invalid (missing API token or bad credentials).
- **`403 Forbidden`**: Client is authenticated, but lacks permissions to access the resource.
- **`404 Not Found`**: Target endpoint or resource ID does not exist.
- **`405 Method Not Allowed`**: The HTTP verb used is not supported by the target endpoint.
- **`409 Conflict`**: Request conflicts with current server state (e.g., duplicate IP or hostname).
- **`429 Too Many Requests`**: Rate limit exceeded (throttled by the server).

### 🟣 5xx Server Errors (Failures on the host/appliance)
- **`500 Internal Server Error`**: Generic server error (unexpected condition on the target host).
- **`502 Bad Gateway`**: Invalid response from upstream server or proxy.
- **`503 Service Unavailable`**: Server is overloaded or down for maintenance.
- **`504 Gateway Timeout`**: Upstream server failed to respond in time (common on slow network operations).

---

## `curl` vs. Python `requests`

Both `curl` and Python's `requests` library interact with REST APIs over HTTP, but they serve completely different phases of API automation.

### Comparison Table

| Feature | `curl` (Command Line) | Python `requests` (Programmatic) |
| :--- | :--- | :--- |
| **Primary Use Case** | Ad-hoc testing, quick debugging, shell scripts | Production automation, CI/CD pipelines, SDK development |
| **JSON Handling** | Requires manual escaping or shell tools like `jq` | Native Python `dict` serialization (`json=payload`) |
| **Error Handling** | Checks exit codes ($?); parsing error messages is manual | Native try/except handling with `response.raise_for_status()` |
| **Session Control** | Cookie files or re-authenticating per request | `requests.Session()` handles cookies/headers automatically |
| **Extensibility** | Limited to shell scripting capabilities | Integrates with database modules, multi-threading, and logic |

### Side-by-Side Example: Authenticated `POST` Request

#### **Using `curl`**
```bash
curl -X POST [https://api.example.com/v1/devices](https://api.example.com/v1/devices) \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "switch-01",
    "ip_address": "192.168.1.10",
    "enabled": true
  }'

Using Python requests
import requests

url = "[https://api.example.com/v1/devices](https://api.example.com/v1/devices)"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}
payload = {
    "hostname": "switch-01",
    "ip_address": "192.168.1.10",
    "enabled": True
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
    print("Device created successfully:", response.json())
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} - Response: {response.text}")
except Exception as err:
    print(f"Other error occurred: {err}")

Enterprise Network Automation Links
Quick reference developer links for automating enterprise network hardware via REST APIs:
🔹 Cisco Systems
 * Cisco Developer Network (DevNet): developer.cisco.com
 * Cisco Meraki Dashboard API: Meraki API v1 Reference
 * Cisco ISE REST API: Cisco ISE API Reference & cURL Guides
 * Cisco Catalyst Center (DNA Center): DNA Center Intent API Reference
🔹 Fortinet (FortiGate)
 * Fortinet Developer Network (FNDN): fndn.fortinet.net (Requires access registration)
 * FortiGate FortiOS REST API Reference: Fortinet Document Library
 * FortiManager JSON/REST API: FortiManager API Documentation
🔹 Palo Alto Networks
 * Palo Alto Networks Developer Portal: pan.dev
 * PAN-OS REST API Guide: pan.dev/panos/docs/restapi
 * PAN-OS Python SDK (pan-os-python): pan-os-python Documentation
 * Palo Alto Networks GitHub: github.com/PaloAltoNetworks
🔹 Arista Networks
 * Arista eAPI Documentation: Arista eAPI Guide
 * Arista PyEAPI Library: github.com/arista-eosplus/pyeapi
🔹 Juniper Networks
 * Juniper TechLibrary API Reference: Juniper REST API Reference
 * PyEZ (Python library for Junos): Juniper PyEZ GitHub

