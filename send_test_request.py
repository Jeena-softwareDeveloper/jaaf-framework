import requests
import json

url = "http://127.0.0.1:8000/api/chat"
data = {"message": "Hello from testing"}
headers = {"Content-Type": "application/json"}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
