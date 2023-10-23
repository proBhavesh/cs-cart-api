# example usage
from api.vendors import VendorsService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize SessionStore and AuthService
vendor_service = VendorsService(vendor_email, vendor_api_key)

# Use AuthService to send authentication requests
# json_response = vendor_service.get_vendors()
# json_response = vendor_service.get_vendor(1)
vendor_data = {
    "company": "New Company1",
    "company_id":"1",
    "storefront": "new_storefront1",
    "email": "newpany@exa1mple.com",
    "phone": "09876541321",
    "address": "456 New Street",
    "city": "Newcity",
    "country": "US",
    "state": "02",
    "zipcode": "654321",
}
json_response = vendor_service.create_vendor(vendor_data)
# json_response = vendor_service.update_vendor(parameter need to pass)
# json_response = vendor_service.delete_vendor(parameter need to pass)



print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
