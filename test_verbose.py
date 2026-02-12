import requests
import json

url = "http://127.0.0.1:8000/api/v1/auth/register"
data = {
    "email": "testuser123@example.com",
    "password": "password123",
    "full_name": "Test User 123"
}

print(f"Sending POST request to: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        try:
            print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        except:
            print("Could not parse as JSON")
    
except requests.exceptions.Timeout:
    print("Request timed out")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
