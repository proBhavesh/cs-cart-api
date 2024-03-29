from typing import Any, Dict
import requests
import json
from api import BASE_URL, encode_credentials


class OrderService:
    def __init__(self, vendor_email: str, vendor_api_key: str):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = BASE_URL

    def send_auth_request(self) -> Any | Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            response = requests.get(url=self.url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response: Any) -> Dict:
        try:
            response.raise_for_status()
            json_response = response.json()
            return json_response
        except (requests.exceptions.HTTPError, json.JSONDecodeError) as e:
            print(f"Error: {e}")
            return {"Error": str(e)}
