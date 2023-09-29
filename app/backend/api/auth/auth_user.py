import os
import base64
import requests
import json
from api.store import SessionStore

# Importing the global data file to access the BASE_URL
from backend.global_data import BASE_URL


class AuthService:
    # The URL parameter is now optional and defaults to None
    def __init__(
        self,
        session_store,
        admin_email,
        admin_api_key,
        url=None,
    ):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")
        self.session_store = session_store
        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()
        # If no URL is provided, it defaults to BASE_URL from the global_data file
        self.url = url if url else BASE_URL

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
