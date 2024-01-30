from typing import Any, Dict, Optional
import requests
import json

# from dotenv import load_dotenv TODO

from api import BASE_URL, encode_credentials


class OrdersService:
    def __init__(self, email, api_key, url=BASE_URL):
        if not email or not api_key:
            raise ValueError("Email and API key must be set")

        self.credentials = encode_credentials(email, api_key)
        self.url = url + "/api/orders/"  # TODO: Wrong Assumption Verified

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
        try:
            response = requests.get(self.url + str(order_id), headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_order(
        self, order_data: Dict
    ) -> Any | Dict[str, str]:  # TODO: Verify order data hint
        try:
            response = requests.post(
                url=self.url, headers=self.headers, json=order_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_order(
        self, order_id: int, order_data: Dict
    ) -> Any | Dict[str, str]:  # TODO: Verify order data hint
        try:
            response = requests.put(
                url=self.url + str(order_id), headers=self.headers, json=order_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_order(self, order_id: int) -> int | Dict[str, str]:
        try:
            response = requests.delete(url=self.url + str(order_id), headers=self.headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            try:
                json_response = response.json()
                print(json_response)
                return json_response
            except json.JSONDecodeError:
                raise ValueError("Response from server was not valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
