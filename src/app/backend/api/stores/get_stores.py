import os
import base64
import requests
import json
from dotenv import load_dotenv

from ..shared.global_data import BASE_URL


class StoresService:
    def __init__(self, store_email, store_api_key, url=None):
        if not store_email or not store_api_key:
            raise ValueError("Store email and API key must be set")

        self.credentials = base64.b64encode(
            f"{store_email}:{store_api_key}".encode()
        ).decode()
        # self.url = url if url else BASE_URL + "/api/products/"
        self.url = url if url else BASE_URL + "/api/stores/"
        self.shipping_url = BASE_URL + "/api/shippings/"

    def get_stores(self, params={}):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url, headers=headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_store(self, store_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url+str(store_id), headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_store(self, store_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.post(
                self.url, headers=headers, json=store_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_store(self, store_id, store_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.put(
                self.url + str(store_id), headers=headers, json=store_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_store(self, store_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.delete(
                self.url + str(store_id), headers=headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_methods(self, params={}):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(
                self.shipping_url, headers=headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_shipping_method(self, shipping_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(
                self.shipping_url + str(shipping_id), headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_shipping_method(self, shipping_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.post(
                self.shipping_url, headers=headers, json=shipping_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_shipping_method(self, shipping_id, shipping_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.put(
                self.shipping_url + str(shipping_id), headers=headers, json=shipping_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_shipping_method(self, shipping_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.delete(
                self.shipping_url + str(shipping_id), headers=headers)
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
                print(response.text)
                raise ValueError("Response from server was not a valid JSON")
        else:
            print(response.content)
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
