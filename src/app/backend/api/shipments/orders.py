from typing import Any, Dict, Optional
import requests
import json
from api import BASE_URL, encode_credentials


class OrderService:
    # The URL parameter is now optional and defaults to None
    def __init__(
        self,
        vendor_email: str,
        vendor_api_key: str,
        url: Optional[str] = None,
    ):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = url if url else BASE_URL

    def send_auth_request(self) -> Any | Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            response = requests.get(self.url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                return json_response

            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
