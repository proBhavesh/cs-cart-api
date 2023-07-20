from api.auth import AuthService
from api.store import SessionStore
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
