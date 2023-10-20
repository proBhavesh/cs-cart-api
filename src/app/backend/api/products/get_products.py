import os
import base64
import requests
import json
from dotenv import load_dotenv

from global_data import (
    BASE_URL,
)


class ProductsService:
    # The URL parameter is now optional and defaults to None
    def __init__(
        self,
        vendor_email,
        vendor_api_key,
        url=None,
    ):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")
        self.credentials = base64.b64encode(
            f"{vendor_email}:{vendor_api_key}".encode()
        ).decode()
        # If no URL is provided, it defaults to BASE_URL from the global_data file
        self.url = url if url else BASE_URL + "/api/products/"

    def get_products(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            response = requests.get(self.url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_product(
        self, product_name, category_ids, price, vendor_id=None, image_pairs=None
    ):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        payload = {
            "product": product_name,
            "category_ids": category_ids,
            "price": price,
        }

        if vendor_id:
            payload["vendor_id"] = vendor_id

        if image_pairs:
            payload["image_pairs"] = image_pairs

        try:
            response = requests.post(self.url, headers=headers, json=payload)
            return self._handle_response(response)
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
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
