import json
from typing import Any, Dict
from urllib.parse import urljoin
import requests

from api import BASE_URL, encode_credentials


class AuthService:
    def __init__(
        self,
        admin_email: str,
        admin_api_key: str,
    ):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email, API key and Session store must be set")

        self.credentials = encode_credentials(admin_email, admin_api_key)
        self.url = urljoin(BASE_URL, "/api/auth")


    def send_auth_request(self, user_email) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        data = {"email": user_email}

        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response) -> Dict[str, Any]:
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                # self.session_store.store_session_key(user_email, json_response["key"])
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
