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
        return self._handle_request(method="GET", params=params)

    def get_store(self, store_id: int) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="GET")

    def create_store(self, store_data: Dict[str, Any]) -> Any | Dict[str, str]:
        return self._handle_request(method="POST", json=store_data)

    def update_store(
        self, store_id: int, store_data: Dict[str, Any]
    ) -> Any | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="PUT", json=store_data)

    def delete_store(self, store_id: int) -> int | Dict[str, str]:
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="DELETE")
        # try:
        #     response = requests.delete(url=url, headers=self.headers)
        #     return response.status_code
        # except requests.exceptions.RequestException as e:
        #     return {"Error": str(e)}

    def get_shipping_methods(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        return self._handle_request(url=self.shipping_url, method="GET", params=params)

    def get_shipping_method(self, shipping_id: int) -> Any | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
        self._handle_request(url=url, method="GET")

    def create_shipping_method(self, shipping_data: Dict[str, Any]) -> Any | Dict[str, str]:
        return self._handle_request(
            url=self.shipping_url, method="POST", json=shipping_data
        )

    def update_shipping_method(self, shipping_id: int, shipping_data: Dict[str, Any]) -> Any | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
        return self._handle_request(url=url, method="PUT", json=shipping_data)

    def delete_shipping_method(self, shipping_id: int) -> int | Dict[str, str]:
        url = urljoin(self.shipping_url, str(shipping_id))
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
