from base64 import b64encode
from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
import json

from api import BASE_URL, encode_credentials


class APIKeyGeneratorService:
    def __init__(self, admin_email: str, admin_api_key: str):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")

        self.credentials = encode_credentials(admin_email, admin_api_key)
        self.url = urljoin(BASE_URL, "/api/generateAPIKey")

    def generate_api_key(self, vendor_email: str) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        payload = json.dumps({"vendor_email": vendor_email})

        try:
            response = requests.post(url=self.url, headers=headers, data=payload)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response: Any) -> Dict:
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                return json_response
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(f"Request failed with status code {response.status_code}")