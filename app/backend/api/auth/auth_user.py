import os
import base64
import requests
import json
from dotenv import load_dotenv
from api.store import SessionStore  # Adjusted import statement


class AuthService:
    def __init__(
        self,
        session_store,
        admin_email,
        admin_api_key,
        url="https://shop.migoiq.app/api/auth",
    ):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")
        self.session_store = session_store
        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()
        self.url = url

    def send_auth_request(self, user_email):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        data = {"email": user_email}

        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            return self._handle_response(user_email, response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, user_email, response):
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                self.session_store.store_session_key(user_email, json_response["key"])
                return {
                    "Session Key": json_response["key"],
                    "Authentication Link": json_response["link"],
                }
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )


# example usage
# from auth.authuser import AuthService
# from store.session_store import SessionStore
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# admin_email = os.getenv("ADMIN_EMAIL")
# admin_api_key = os.getenv("ADMIN_API_KEY")

# # Initialize SessionStore and AuthService
# session_store = SessionStore()
# auth_service = AuthService(session_store, admin_email, admin_api_key)

# # Use AuthService to send authentication requests
# print(auth_service.send_auth_request("vendor2@example.com"))
# # print(auth_service.send_auth_request("vendor2@example.com"))
