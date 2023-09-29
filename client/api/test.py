from auth.authuser import AuthService
from store.session_store import SessionStore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
admin_api_key = os.getenv("ADMIN_API_KEY")

# Initialize SessionStore and AuthService
session_store = SessionStore()
auth_service = AuthService(session_store, admin_email, admin_api_key)

# Use AuthService to send authentication requests
print(auth_service.send_auth_request("vendor@example.com"))
# print(auth_service.send_auth_request("vendor2@example.com"))

# # Import GetPagesService class from GetPagesService.py
# from getpages import GetPagesService

# # Initialize GetPagesService with admin email and API key
# get_pages_service = GetPagesService(
#     "vendor@example.com", "1T5W3C21870R410Y47c814Rck3l2v215"
# )

# # Define parameters for the GET request
# params = {
#     "page": 1,
#     "items_per_page": 10,
#     "sort_by": "position",
#     "sort_order": "desc",
# }

# # Send request to get pages with parameters
# response = get_pages_service.send_pages_request(params)

# # Print the response
# print(response)
