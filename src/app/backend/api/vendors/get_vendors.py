import json
from urllib.parse import urljoin
import requests
from typing import Any, Dict, Optional

from api import BASE_URL, encode_credentials


class VendorsService:
    def __init__(
        self, vendor_email: str, vendor_api_key: str, url: Optional[str] = None
    ):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")
        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = url if url else BASE_URL + "/api/vendors/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_vendors(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        try:
            response = requests.get(url=self.url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_vendor(self, vendor_id) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        try:
            response = requests.get(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_vendor(self, vendor_data) -> Any | Dict[str, str]:
        try:
            response = requests.post(
                url=self.url, headers=self.headers, json=vendor_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_vendor(self, vendor_id, vendor_data) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        try:
            response = requests.put(url=url, headers=self.headers, json=vendor_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_vendor(self, vendor_id) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        try:
            response = requests.delete(url=url, headers=self.headers)
            return response.status_code
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
