from api.stores import StoresService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize Session and StoresService
store_service = StoresService(vendor_email, vendor_api_key)

# Fetch all stores
json_response = store_service.get_stores()
# json_response = store_service.get_stores(1)

# Create a store
store_data = {
    "company": "Example Company 5",
    "storefront": "examplyy22.com",
    "secure_storefront": "examgpl22.com",
    "clone_from": "2",
    "clone": {
        "layouts": "i",
        "settings": "Yi",
        "products": "Yi",
        "categories": "iY"
    }
}
# json_response = store_service.create_store(store_data)

# Update a store
update_data = {
    "company": "Updated Example",
    "storefront": "updatedexample.com",
    "secure_storefront": "updatedexample.com",
    "countries_list": [
        "GB", "US"
    ],
    "company_name": "Updated new company",
    "company_address": "Updated 41 Avenue"
}
# json_response = store_service.update_store(store_id='store_id', store_data=update_data)

# Delete a store
# json_response = store_service.delete_store(store_id='store_id')

print(json.dumps(json_response, indent=4))