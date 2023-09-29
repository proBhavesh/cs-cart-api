# example usage
from api.shipments import OrderService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

# Initialize SessionStore and AuthService
product_service = OrderService(vendor_email, vendor_api_key)

# Use AuthService to send authentication requests
json_response = product_service.send_auth_request()
print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
