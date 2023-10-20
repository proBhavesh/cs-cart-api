# example usage
from api.products import ProductsService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize SessionStore and AuthService
product_service = ProductsService(vendor_email, vendor_api_key)

# Use AuthService to send authentication requests
json_response = product_service.get_products()
# json_response = product_service.create_product("lenovo laptop", [2], "5000")

print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
