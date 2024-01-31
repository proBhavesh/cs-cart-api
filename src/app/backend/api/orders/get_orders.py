from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
import json

from api import BASE_URL, encode_credentials


class OrdersService:
    def __init__(self, email: str, api_key: str):
        if not email or not api_key:
            raise ValueError("Email and API key must be set")

        self.credentials = encode_credentials(email, api_key)
        self.url = BASE_URL + "/api/orders/"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_orders(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        try:
            response = requests.get(url=self.url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_order(self, order_id: int) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
        try:
            response = requests.get(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_order(self, order_data: Dict[str, Any]) -> Any | Dict[str, str]:
        try:
            response = requests.post(url=self.url, headers=self.headers, json=order_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
        try:
            response = requests.put(url=url, headers=self.headers, json=order_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_order(self, order_id: int) -> int | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
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
                raise ValueError("Response from server was not valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
