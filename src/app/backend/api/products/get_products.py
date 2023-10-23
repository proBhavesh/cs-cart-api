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
        self.product_variation_groups_url = BASE_URL + "/api/product_variations_groups/"
        self.features_url = BASE_URL + "/api/features/"
        self.base_url = (url if url else BASE_URL) + "/api/combinations/"
        self.exceptions_url = (url if url else BASE_URL) + "/api/exceptions/"

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

    def update_product(self, product_id, product_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        url = f"{self.url}{product_id}"

        try:
            response = requests.put(url, headers=headers, json=product_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_product(self, product_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        url = f"{self.url}{product_id}"

        try:
            response = requests.delete(url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_product_features(self, product_id):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}"}
        try:
            response = requests.get(
                self.url + str(product_id) + "/features", headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_product_features(self, product_id, product_data):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}"}
        try:
            response = requests.put(
                self.url + str(product_id), headers=headers, json=product_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    # Feature related methods
    def get_features(self, params={}):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}", }
        try:
            response = requests.get(
                self.features_url, headers=headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_feature(self, feature_id):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}", }
        try:
            response = requests.get(
                self.features_url + str(feature_id), headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_feature(self, feature_data):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}", }
        try:
            response = requests.post(
                self.features_url, headers=headers, json=feature_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_feature(self, feature_id, feature_data):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}", }
        try:
            response = requests.put(
                self.features_url + str(feature_id), headers=headers, json=feature_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_feature(self, feature_id):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.credentials}", }
        try:
            response = requests.delete(
                self.features_url + str(feature_id), headers=headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_product_variations(self, group_id):
        response = requests.get(
            f"{self.url}?variation_group_id={group_id}", headers=self.headers)
        return self._handle_response(response)

    def add_product_to_group(self, id, data):
        response = requests.put(
            f"{self.url}{id}", headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def detach_product_variation(self, id):
        response = requests.post(
            f"{self.url}{id}/detach_product_variation", headers=self.headers)
        return self._handle_response(response)

    def set_default_variation(self, id):
        response = requests.post(
            f"{self.url}{id}/set_default_product_variation", headers=self.headers)
        return self._handle_response(response)

    def generate_variations(self, id, combinations):
        data = {"combinations": combinations}
        response = requests.post(
            f"{self.url}{id}/generate_product_variations", headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def create_variation_group(self, data):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.post(
            self.product_variation_groups_url, headers=headers, data=json.dumps(data))
        return self._handle_response(response)

    def get_variation_groups(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.get(
            self.product_variation_groups_url, headers=headers)
        return self._handle_response(response)

    def get_variation_group(self, id_or_code):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.get(
            self.product_variation_groups_url + id_or_code, headers=headers)
        return self._handle_response(response)

    def update_variation_group(self, id_or_code, data):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.put(self.product_variation_groups_url +
                                id_or_code, headers=headers, data=json.dumps(data))
        return self._handle_response(response)

    def delete_variation_group(self, id_or_code):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.delete(
            self.product_variation_groups_url + id_or_code, headers=headers)
        return self._handle_response(response)

    def list_product_options(self, product_id):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.get(
            self.url + f"{product_id}/options", headers=headers)
        return self._handle_response(response)

    def get_specific_option(self, option_id):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.get(
            self.url + f"options/{option_id}", headers=headers)
        return self._handle_response(response)

    def create_option(self, data):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.post(
            self.url + "options/", headers=headers, data=json.dumps(data))
        return self._handle_response(response)

    def update_option(self, option_id, data):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.put(
            self.url + f"options/{option_id}", headers=headers, data=json.dumps(data))
        return self._handle_response(response)

    def delete_option(self, option_id):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + self.credentials}
        response = requests.delete(
            self.url + f"options/{option_id}", headers=headers)
        return self._handle_response(response)

    def list_option_combinations(self, product_id, items_per_page=None, page=None):
        params = {'product_id': product_id}
        if items_per_page:
            params['items_per_page'] = items_per_page
        if page:
            params['page'] = page
        response = requests.get(self.base_url, params=params, headers={
                                'Authorization': self.credentials})
        return self._handle_response(response)

    def get_option_combination(self, combination_hash):
        url = self.base_url + combination_hash
        response = requests.get(
            url, headers={'Authorization': self.credentials})
        return self._handle_response(response)

    def create_option_combination(self, product_id, combination, amount=None, position=None):
        data = {'product_id': product_id, 'combination': combination}
        if amount:
            data['amount'] = amount
        if position:
            data['position'] = position
        response = requests.post(self.base_url, data=data, headers={
                                 'Authorization': self.credentials})
        return self._handle_response(response)

    def update_option_combination(self, combination_hash, product_code=None, amount=None, position=None):
        data = {}
        if product_code:
            data['product_code'] = product_code
        if amount:
            data['amount'] = amount
        if position:
            data['position'] = position
        url = self.base_url + combination_hash
        response = requests.put(url, data=data, headers={
                                'Authorization': self.credentials})
        return self._handle_response(response)

    def delete_option_combination(self, combination_hash, product_id):
        url = self.base_url + combination_hash
        params = {'product_id': product_id}
        response = requests.delete(url, params=params, headers={
                                   'Authorization': self.credentials})
        return self._handle_response(response)


# list exceptions

    def list_exceptions(self, product_id):
        response = requests.get(self.exceptions_url, params={
                                "product_id": product_id}, headers={'Authorization': self.credentials})
        return self._handle_response(response)

    def get_exception(self, exception_id):
        url = self.exceptions_url + exception_id
        response = requests.get(
            url, headers={'Authorization': self.credentials})
        return self._handle_response(response)

    def create_exception(self, product_id, combination):
        data = {"product_id": product_id, "combination": combination}
        response = requests.post(self.exceptions_url, data=data, headers={
                                 'Authorization': self.credentials})
        return self._handle_response(response)

    def update_exception(self, exception_id, combination):
        data = {"combination": combination}
        url = self.exceptions_url + exception_id
        response = requests.put(url, data=data, headers={
                                'Authorization': self.credentials})
        return self._handle_response(response)

    def delete_exception(self, exception_id, product_id):
        url = self.exceptions_url + exception_id
        response = requests.delete(url, params={"product_id": product_id}, headers={
                                   'Authorization': self.credentials})
        return self._handle_response(response)

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
