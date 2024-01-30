import json
import requests
from typing import Any, Dict, Optional

from api import BASE_URL, encode_credentials


class StoresService:
    def __init__(self, store_email: str, store_api_key: str, url: Optional[str] = None):
        if not store_email or not store_api_key:
            raise ValueError("Store email and API key must be set")

        self.credentials = encode_credentials(store_email, store_api_key)
        self.url = url if url else BASE_URL + "/api/stores/"
        self.shipping_url = BASE_URL + "/api/shippings/"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_stores(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        try:
            response = requests.get(self.url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_store(self, store_id)-> Any | Dict[str, str]:
        try:
            response = requests.get(self.url + str(store_id), headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_store(self, store_data)-> Any | Dict[str, str]:
        try:
            response = requests.post(self.url, headers=self.headers, json=store_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_store(self, store_id: int, store_data)-> Any | Dict[str, str]:
        try:
            response = requests.put(
                self.url + str(store_id), headers=self.headers, json=store_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_store(self, store_id)-> int | Dict[str, str]:
        try:
            response = requests.delete(self.url + str(store_id), headers=self.headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_methods(self, params={})-> Any | Dict[str, str]:
        try:
            response = requests.get(
                self.shipping_url, headers=self.headers, params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_method(self, shipping_id)-> Any | Dict[str, str]:
        try:
            response = requests.get(
                self.shipping_url + str(shipping_id), headers=self.headers
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_shipping_method(self, shipping_data)-> Any | Dict[str, str]:
        try:
            response = requests.post(
                self.shipping_url, headers=self.headers, json=shipping_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_shipping_method(self, shipping_id, shipping_data)-> Any | Dict[str, str]:
        try:
            response = requests.put(
                self.shipping_url + str(shipping_id),
                headers=self.headers,
                json=shipping_data,
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_shipping_method(self, shipping_id) -> int | Dict[str, str]:
        try:
            response = requests.delete(
                self.shipping_url + str(shipping_id), headers=self.headers
            )
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            try:
                json_response = response.json()
                # print(json_response)
                return json_response
            except json.JSONDecodeError:
                # print(response.text)
                raise ValueError("Response from server was not a valid JSON")
        else:
            print(response.content)
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
