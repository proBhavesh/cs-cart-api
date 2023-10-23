import os
import base64
import requests
import json
from dotenv import load_dotenv

from global_data import (
    BASE_URL,
)


class VendorsService:
    def __init__(self, vendor_email, vendor_api_key, url=None):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")
        self.credentials = base64.b64encode(
            f"{vendor_email}:{vendor_api_key}".encode()
        ).decode()
        self.url = url if url else BASE_URL + "/api/vendors/"

    def get_vendors(self, params={}):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url, headers=headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_vendor(self, vendor_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.get(self.url+str(vendor_id), headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_vendor(self, vendor_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.post(self.url, headers=headers, json=vendor_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_vendor(self, vendor_id, vendor_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.put(
                self.url + str(vendor_id), headers=headers, json=vendor_data
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_vendor(self, vendor_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        try:
            response = requests.delete(self.url + str(vendor_id), headers=headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
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