API Authentication Cheatsheet
A comprehensive guide and reference for common API authentication schemes using cURL and Python (requests).
Quick Reference Guide
| Authentication Type | Common Use Case |
|---|---|
| Public API | Open APIs, public data feeds |
| Basic Auth | Legacy applications, internal/admin APIs |
| API Key | Developer portals, rate-limited public APIs |
| Bearer Token | REST APIs, FortiGate |
| JWT | Microservices, stateless authentication |
| OAuth 2.0 | Cloud APIs (Microsoft Graph, Google, GitHub) |
| Session / Cookie | Web applications, browser-based APIs |
| FortiGate API | FortiGate network monitoring |
| mTLS | High-security APIs, Banking, B2B enterprise integrations |
| HMAC | AWS services, payment gateways, webhook verification |
1. No Authentication (Public API)
Public endpoints that do not require any credentials or tokens.
cURL
curl https://api.example.com/logio

Python
import requests

r = requests.get("https://api.example.com/logio")
print(r.json())

2. Basic Authentication
Credentials are Base64 encoded as username:password.
cURL
# Using cURL flag
curl -u admin:Password123 \
  https://api.example.com/logio

# Or using explicit header
curl -H "Authorization: Basic YWRtaW46UGFzc3dvcmQxMjM=" \
  https://api.example.com/users

Python
import requests

response = requests.get(
    "https://api.example.com/users",
    auth=("admin", "Password123")
)

print(response.json())

3. API Key Authentication
API Key in Header
cURL
curl \
  -H "X-API-Key: abc123xyz" \
  https://api.example.com/logio

Python
import requests

headers = {
    "X-API-Key": "abc123xyz"
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)

API Key in Query String
cURL
curl "https://api.example.com/logio?apikey=abc123xyz"

Python
import requests

params = {
    "apikey": "abc123xyz"
}

response = requests.get(
    "https://api.example.com/logio",
    params=params
)

4. Bearer Token Authentication
Most common for REST APIs including FortiGate.
cURL
curl \
  -H "Authorization: Bearer eyJhbGciOi..." \
  https://api.example.com/logio

Python
import requests

headers = {
    "Authorization": "Bearer eyJhbGciOi..."
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)

5. JWT Authentication
JWT is usually passed as a Bearer token.
Example JWT Structure:
Header    : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Payload   : eyJ1c2VyIjoiYWRtaW4ifQ
Signature : signature

cURL
curl \
  -H "Authorization: Bearer JWT_TOKEN" \
  https://api.example.com/logio

Python
import requests

headers = {
    "Authorization": "Bearer JWT_TOKEN"
}

response = requests.get(
    "https://api.example.com/logio",
    headers=headers
)

6. OAuth 2.0
Used by Microsoft Graph, Google, GitHub, etc.
Get Access Token
cURL
curl -X POST \
  https://login.microsoftonline.com/TENANT/oauth2/v2.0/token \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "grant_type=client_credentials"

Python
import requests

token_url = "https://login.microsoftonline.com/TENANT/oauth2/v2.0/token"

token = requests.post(
    token_url,
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
)

Use Token
cURL
curl \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  https://graph.microsoft.com/v1.0/users

7. Session / Cookie Authentication
Login first, then use the session cookie for future requests.
cURL
# Login and save cookies
curl -c cookies.txt \
  -X POST \
  -d "user=admin&password=password" \
  https://example.com/logio

# Next request using saved cookies
curl -b cookies.txt \
  https://example.com/profile

Python
import requests

session = requests.Session()

session.post(
    "https://example.com/logio",
    data={
        "user": "admin",
        "password": "password"
    }
)

r = session.get(
    "https://example.com/profile"
)

8. FortiGate API Token Authentication
Most common in FortiGate monitoring.
cURL
curl -k \
  -H "Authorization: Bearer FGT_TOKEN" \
  https://x.x.x.x/api/v2/monitor/system/status

Python
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

9. Client Certificate Authentication (mTLS)
Client presents certificate and private key.
cURL
curl \
  --cert client.crt \
  --key client.key \
  https://api.example.com/data

Python
import requests

response = requests.get(
    "https://api.example.com/data",
    cert=("client.crt", "client.key")
)

10. HMAC Authentication
Used by AWS and payment gateways.
cURL
curl \
  -H "Authorization: HMAC SIGNATURE" \
  https://api.example.com

Python
import hmac
import hashlib

secret = b"secret"

signature = hmac.new(
    secret,
    b"message",
    hashlib.sha256
).hexdigest()

print(signature)

Appendix: Test with cURL (FortiGate Examples)
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

