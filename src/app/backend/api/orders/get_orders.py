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
        self.url = urljoin(BASE_URL, "/api/orders/")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_orders(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        return self._handle_request(method="GET", params=params)

    def get_order(self, order_id: int) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="GET")

    def create_order(self, order_data: Dict[str, Any]) -> Any | Dict[str, str]:
        return self._handle_request(method="POST", json=order_data)

    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="PUT", json=order_data)

    def delete_order(self, order_id: int) -> int | Dict[str, str]:
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="DELETE")
        # try:
        #     response = requests.delete(url=url, headers=self.headers)
        #     return response.status_code
        # except requests.exceptions.RequestException as e:
        #     return {"Error": str(e)}

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
                response = requests.get(url=_url, headers=_headers, params=params)
            elif method == "POST":
                response = requests.post(url=_url, headers=_headers, json=json)
            elif method == "PUT":
                response = requests.put(url=_url, headers=_headers, json=json)
            elif method == "DELETE":
                response = requests.delete(url=_url, headers=_headers)
            else:
                raise ValueError("Unsupported HTTP method")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"RequestException ({method}): {e}")
            return {"Error": str(e)}
