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
       
        self.url = urljoin(BASE_URL, "/api/vendors/")
        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_vendors(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        return self._handle_request(method="GET", params=params)

    def get_vendor(self, vendor_id) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        return self._handle_request(url=url, method="GET")

    def create_vendor(self, vendor_data) -> Any | Dict[str, str]:
        return self._handle_request(method="POST", json=vendor_data)

    def update_vendor(self, vendor_id, vendor_data) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        return self._handle_request(url=url, method="PUT", json=vendor_data)

    def delete_vendor(self, vendor_id) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(vendor_id))
        return self._handle_request(url=url, method="DELETE")

    def _handle_response(self, response: Any) -> Dict:
        try:
            response.raise_for_status()
            json_response = response.json()
            return json_response
        except (requests.exceptions.HTTPError, json.JSONDecodeError) as e:
            print(f"Error: {e}")
            return {"Error": str(e)}

    def _handle_request(
        self,
        *,
        url: Optional[str] = None,
        method: Optional[str] = None,
        headers: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any | Dict[str, int | str]:
        if url:
            _url = url
        else:
            _url = self.url

        if headers:
            _headers = headers
        else:
            _headers = self.headers

        try:
            if method == "GET":
                response = requests.get(
                    url=_url, headers=_headers, params=params, data=data
                )
            elif method == "POST":
                response = requests.post(
                    url=_url, headers=_headers, json=json, data=data
                )
            elif method == "PUT":
                response = requests.put(
                    url=_url, headers=_headers, json=json, data=data
                )
            elif method == "DELETE":
                response = requests.delete(url=_url, headers=_headers)
            else:
                raise ValueError("Unsupported HTTP method")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"RequestException ({method}): {e}")
            return {"Error": str(e)}
