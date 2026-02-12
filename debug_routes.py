import requests
import sys

base_url = "http://127.0.0.1:8000"

def check(path):
    url = f"{base_url}{path}"
    try:
        resp = requests.get(url)
        print(f"{path}: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Content-Type: {resp.headers.get('Content-Type')}")
            print(f"Start of content: {resp.text[:100]}")
    except Exception as e:
        print(f"{path}: Error {e}")

print("Checking endpoints...")
check("/api/health")
check("/api/v1/openapi.json")
check("/index.html")
check("/")
