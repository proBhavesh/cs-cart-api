import json
from urllib.parse import urljoin
import requests
from typing import Any, Dict, Optional

from api import BASE_URL, encode_credentials


class StoresService:
    def __init__(self, store_email: str, store_api_key: str):
        if not store_email or not store_api_key:
            raise ValueError("Store email and API key must be set")

        self.url = urljoin(BASE_URL, "/api/stores/")
        self.shipping_url = urljoin(BASE_URL, "/api/shippings/")

        self.credentials = encode_credentials(store_email, store_api_key)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_stores(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        try:
            response = requests.get(url=self.url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_store(self, store_id) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        try:
            response = requests.get(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_store(self, store_data) -> Any | Dict[str, str]:
        try:
            response = requests.post(self.url, headers=self.headers, json=store_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_store(self, store_id: int, store_data) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        try:
            response = requests.put(url=url, headers=self.headers, json=store_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_store(self, store_id) -> int | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        try:
            response = requests.delete(url=url, headers=self.headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_methods(self, params: Dict = {}) -> Any | Dict[str, str]:
        try:
            response = requests.get(url=self.shipping_url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_method(self, shipping_id) -> Any | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
        try:
            response = requests.get(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_shipping_method(self, shipping_data) -> Any | Dict[str, str]:
        try:
            response = requests.post(url=self.shipping_url, headers=self.headers, json=shipping_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_shipping_method(self, shipping_id, shipping_data) -> Any | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
        try:
            response = requests.put(url=url,headers=self.headers,json=shipping_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_shipping_method(self, shipping_id) -> int | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
        try:
            response = requests.delete(url=url, headers=self.headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            try:
                json_response = response.json()
                return json_response
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(f"Request failed with status code {response.status_code}")
