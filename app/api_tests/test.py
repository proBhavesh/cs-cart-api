# example usage
from api.api_key_generation import APIKeyGeneratorService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
admin_api_key = os.getenv("ADMIN_API_KEY")

# Initialize SessionStore and AuthService
api_key_service = APIKeyGeneratorService(admin_email, admin_api_key)

# Use AuthService to send authentication requests
json_response = api_key_service.generate_api_key(vendor_email="vendor@example.com")
print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
