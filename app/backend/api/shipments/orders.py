import os
import base64
import requests
import json
from dotenv import load_dotenv


class OrderService:
    def __init__(
        self,
        vendor_email,
        vendor_api_key,
        url="https://shop.migoiq.app/api/orders",
    ):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")
        self.credentials = base64.b64encode(
            f"{vendor_email}:{vendor_api_key}".encode()
        ).decode()
        self.url = url

    def send_auth_request(self):
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
