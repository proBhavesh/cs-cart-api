import os
import base64
import requests
import json
from dotenv import load_dotenv

from ..shared.global_data import BASE_URL


class OrdersService:
    def __init__(self, email, api_key, url=BASE_URL):
        if not email or not api_key:
            raise ValueError("Email and API key must be set")
        self.credentials = base64.b64encode(
            f"{email}:{api_key}".encode()).decode()
        self.url = url + "/api/orders/"

    def get_orders(self, params={}):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url, headers=headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_order(self, order_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url + str(order_id), headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_order(self, order_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.post(
                self.url, headers=headers, json=order_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_order(self, order_id, order_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.put(
                self.url + str(order_id), headers=headers, json=order_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_order(self, order_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.delete(
                self.url + str(order_id), headers=headers)
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
