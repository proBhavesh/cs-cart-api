# example usage
from api.orders import OrdersService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize SessionStore and AuthService
orders_service = OrdersService(vendor_email, vendor_api_key)


# json_response = orders_service.get_orders()
# json_response = orders_service.get_order(order_id=1)

# Create an order
order_data = {
    "user_id": "0",
    "payment_id": "2",
    "shipping_id": "1",
    "products": {
        "1": {
            "product_id": "12",
            "amount": "1"
        },
        "2": {
           "product_id": "13",
           "amount":"2"
        }
    },
    "user_data": {
        "email": "guest@example.com",
        "firstname": "Guest",
        "lastname": "Guest",
        "s_firstname": "Guest",
        "s_lastname": "Guest",
        "s_country": "US",
        "s_city": "Boston",
        "s_state": "MA",
        "s_zipcode": "02125",
        "s_address": "44 Main street",
        "b_firstname": "Guest",
        "b_lastname": "Guest",
        "b_country": "US",
        "b_city": "Boston",
        "b_state": "MA",
        "b_zipcode": "02125",
        "b_address": "44 Main street"
    }
}
json_response =  orders_service.create_order(order_data)

# Update an order
update_data = {
   "status": "P",
    "user_data": {
        "email": "newemail@example.com",
    },
    "total": "100"
}
# json_response =  orders_service.update_order(order_id=1, order_data=update_data)

# Use AuthService to send authentication requests
# json_response = orders_service.send_auth_request()



print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
