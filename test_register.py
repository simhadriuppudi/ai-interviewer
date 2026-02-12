import requests

url = "http://127.0.0.1:8000/api/v1/auth/register"
data = {
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
