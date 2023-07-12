import requests
from requests.auth import HTTPBasicAuth
import base64
import json

# Your email and API key
email = "probhavsh@gmail.com"
api_key = "1K2RD9cusR2331Jaiv646Y3717r7dh84"

# Encode the email and API key
credentials = base64.b64encode(f"{email}:{api_key}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
}

response = requests.get("https://shop.migoiq.app/api/auth", headers=headers)
data = json.loads(response.text)

print("Error:", response.status_code)
# # Print the status code and the response text
print(f"Status Code: {response.status_code}")
# # print(f"Response Text: {response.text}")
print(json.dumps(data, indent=4))
