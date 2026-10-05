# API Authentication Methods Cheatsheet

A comprehensive guide and reference for common API authentication schemes using **cURL** and **Python (`requests`)**.

---

## Quick Reference Guide

| Authentication Type | Common Use Case |
| :--- | :--- |
| **Public API** | Open APIs, public data feeds |
| **Basic Auth** | Legacy applications, internal/admin APIs |
| **API Key** | Developer portals, rate-limited public APIs |
| **Bearer Token** | REST APIs, FortiGate |
| **JWT** | Microservices, stateless authentication |
| **OAuth 2.0** | Cloud APIs (Microsoft Graph, Google, GitHub) |
| **Session / Cookie** | Web applications, browser-based APIs |
| **FortiGate API** | FortiGate network monitoring |
| **mTLS** | High-security APIs, Banking, B2B enterprise integrations |
| **HMAC** | AWS services, payment gateways, webhook verification |

---

## 1. No Authentication (Public API)

Public endpoints that do not require any credentials or tokens.

### cURL
```bash
curl https://api.example.com/logio
```

### Python
```python
import requests

response = requests.get("https://api.example.com/logio")
print(response.json())
```

---

## 2. Basic Authentication

Credentials sent as Base64-encoded `username:password` strings in the HTTP header.

### cURL
```bash
# Using cURL flag
curl -u admin:Password123 https://api.example.com/logio

# Explicit Header
curl -H "Authorization: Basic YWRtaW46UGFzc3dvcmQxMjM=" \
  https://api.example.com/users
```

### Python
```python
import requests

response = requests.get(
    "https://api.example.com/users",
    auth=("admin", "Password123")
)

print(response.json())
```

---

## 3. API Key Authentication

API Keys passed either via HTTP headers or directly in query string parameters.

### API Key in Header

#### cURL
```bash
curl -H "X-API-Key: abc123xyz" https://api.example.com/logio
```

#### Python
```python
import requests

headers = {
    "X-API-Key": "abc123xyz"
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)
```

### API Key in Query String

#### cURL
```bash
curl "https://api.example.com/logio?apikey=abc123xyz"
```

#### Python
```python
import requests

params = {
    "apikey": "abc123xyz"
}

response = requests.get(
    "https://api.example.com/logio",
    params=params
)
```

---

## 4. Bearer Token Authentication

Standard security token pattern widely used across REST APIs.

### cURL
```bash
curl -H "Authorization: Bearer eyJhbGciOi..." \
  https://api.example.com/logio
```

### Python
```python
import requests

headers = {
    "Authorization": "Bearer eyJhbGciOi..."
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)
```

---

## 5. JWT (JSON Web Token) Authentication

JWT tokens are typically formatted in three parts (`header.payload.signature`) and passed as a Bearer Token.

```text
Header    : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Payload   : eyJ1c2VyIjoiYWRtaW4ifQ
Signature : signature
```

### cURL
```bash
curl -H "Authorization: Bearer JWT_TOKEN" \
  https://api.example.com/logio
```

### Python
```python
import requests

headers = {
    "Authorization": "Bearer JWT_TOKEN"
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)
```

---

## 6. OAuth 2.0

Token request process followed by authenticated API requests (e.g., Client Credentials Grant).

### Step 1: Request Access Token

#### cURL
```bash
curl -X POST https://login.microsoftonline.com/TENANT/oauth2/v2.0/token \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "grant_type=client_credentials"
```

#### Python
```python
import requests

token_response = requests.post(
    "https://login.microsoftonline.com/TENANT/oauth2/v2.0/token",
    data={
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "grant_type": "client_credentials"
    }
)
access_token = token_response.json().get("access_token")
```

### Step 2: Use Access Token

#### cURL
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  https://graph.microsoft.com/v1.0/users
```

---

## 7. Session / Cookie Authentication

Authenticates once to receive a session cookie, then attaches that cookie to subsequent requests.

### cURL
```bash
# Login and store cookies in file
curl -c cookies.txt -X POST -d "user=admin&password=password" \
  https://example.com/logio

# Subsequent request using saved cookies
curl -b cookies.txt https://example.com/profile
```

### Python
```python
import requests

session = requests.Session()

# Login request
session.post(
    "https://example.com/logio",
    data={
        "user": "admin",
        "password": "password"
    }
)

# Persistent session GET request
response = session.get("https://example.com/profile")
```

---

## 8. FortiGate API Token Authentication

Common method used for FortiGate REST API automation and monitoring.

### cURL
```bash
curl -k -H "Authorization: Bearer FGT_TOKEN" \
  https://x.x.x.x/api/v2/monitor/system/status
```

### Python
```python
import requests

headers = {
    "Authorization": "Bearer FGT_TOKEN"
}

response = requests.get(
    "https://x.x.x.x/api/v2/monitor/system/status",
    headers=headers,
    verify=False
)

print(response.json())
```

---

## 9. Client Certificate Authentication (mTLS)

Mutual TLS authentication where client presents a public certificate and private key.

### cURL
```bash
curl --cert client.crt --key client.key \
  https://api.example.com/data
```

### Python
```python
import requests

response = requests.get(
    "https://api.example.com/data",
    cert=("client.crt", "client.key")
)
```

---

## 10. HMAC Authentication

Hash-based Message Authentication Code used for cryptographic signing of requests.

### cURL
```bash
curl -H "Authorization: HMAC SIGNATURE" \
  https://api.example.com
```

### Python (Signature Generation Example)
```python
import hmac
import hashlib

secret = b"secret"
message = b"message"

signature = hmac.new(
    secret,
    message,
    hashlib.sha256
).hexdigest()

print(f"HMAC Signature: {signature}")
```

---

## Appendix: FortiGate Quick cURL Examples

```bash
# System Status
curl -k -H "Authorization: Bearer TOKEN" \
  https://FGT/api/v2/monitor/system/status

# Resource Usage
curl -k -H "Authorization: Bearer TOKEN" \
  https://FGT/api/v2/monitor/system/resource/usage

# Interface Status
curl -k -H "Authorization: Bearer TOKEN" \
  https://FGT/api/v2/monitor/system/interface

# HA Status
curl -k -H "Authorization: Bearer TOKEN" \
  https://FGT/api/v2/monitor/system/ha-status
```
