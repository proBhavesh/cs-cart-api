from urllib.parse import urljoin
import requests
import json
from typing import Any, Dict

from api import BASE_URL, encode_credentials


class ProductsService:
    def __init__(self, vendor_email: str, vendor_api_key: str):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = urljoin(BASE_URL, "/api/products/")
        self.product_variation_groups_url = urljoin(BASE_URL, "/api/product_variations_groups/")
        self.features_url = urljoin(BASE_URL, "/api/features/")
        self.base_url = urljoin(BASE_URL, "/api/combinations/")
        self.exceptions_url = urljoin(BASE_URL, "/api/exceptions/")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_products(self) -> Any | Dict[str, str]:
        try:
            response = requests.get(self.url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_product(self, payload: Dict[str, Any]) -> Any | Dict[str, int | str]:
        try:
            response = requests.post(url=self.url, headers=self.headers, json=payload)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print("RequestException: ", e)
            return {"Error": str(e)}

    def update_product(self, product_id: int, payload: Dict[str, Any]) -> Any | Dict[str, int | str]:
        url = urljoin(self.url, str(product_id))
        try:
            response = requests.put(url=url, headers=self.headers, json=payload: Dict[str, Any])
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_product(self, product_id: int) -> Any | dict[str, str]:
        url = urljoin(self.url, str(product_id))
        try:
            response = requests.delete(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_product_features(self, product_id: int):
        url = urljoin(self.url, "/features/" + str(product_id))
        try:
            response = requests.get(url=url, headers=self.headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_product_features(self, product_id: int, payload: Dict[str, Any]):
        url = urljoin(self.url, str(product_id))
        try:
            response = requests.put(url=url, headers=self.headers, json=payload)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_features(self, params={}):
        try:
            response = requests.get(
                self.features_url, headers=self.headers, params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_feature(self, feature_id):
        try:
            response = requests.get(
                self.features_url + str(feature_id), headers=self.headers
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def create_feature(self, feature_data):
        try:
            response = requests.post(url=self.features_url, headers=self.headers, json=feature_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def update_feature(self, feature_id: int, feature_data: Dict[str, Any]):
        url = urljoin(self.features_url, str(feature_id))
        try:
            response = requests.put(url, headers=self.headers, json=feature_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def delete_feature(self, feature_id: int):
        url = urljoin(self.features_url, str(feature_id))
        try:
            response = requests.delete(url=url, headers=self.headers)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_product_variations(self, group_id):
        url = urljoin(self.url, f"?variation_group_id={group_id}")
        response = requests.get(url=url, headers=self.headers)
        return self._handle_response(response)

    def add_product_to_group(self, id, data):
        url = urljoin(self.url, str(id))
        response = requests.put(url=url, headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def detach_product_variation(self, id):
        url = urljoin(self.url, f"{id}/detach_product_variation")
        response = requests.post(url=url, headers=self.headers)
        return self._handle_response(response)

    def set_default_variation(self, id):
        url = urljoin(self.url, f"{id}/set_default_product_variation")
        response = requests.post(url=url, headers=self.headers)
        return self._handle_response(response)

    def generate_variations(self, id, combinations):
        url = urljoin(self.url, f"{id}/generate_product_variations")
        response = requests.post(url=url, headers=self.headers, data=json.dumps({"combinations": combinations}))
        return self._handle_response(response)

    def create_variation_group(self, data):
        response = requests.post(url=self.product_variation_groups_url, headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def get_variation_groups(self):
        response = requests.get(self.product_variation_groups_url, headers=self.headers)
        return self._handle_response(response)

    def get_variation_group(self, id_or_code):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        response = requests.get(url=url, headers=self.headers)
        return self._handle_response(response)

    def update_variation_group(self, id_or_code, data):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        response = requests.put(url=url, headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def delete_variation_group(self, id_or_code):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        response = requests.delete(url=url, headers=self.headers)
        return self._handle_response(response)

    def list_product_options(self, product_id):
        url = urljoin(self.url, f"{product_id}/options")
        response = requests.get(url=url, headers=self.headers)
        return self._handle_response(response)

    def get_specific_option(self, option_id):
        url = urljoin(self.url, f"options/{option_id}")
        response = requests.get(url=url, headers=self.headers)
        return self._handle_response(response)

    def create_option(self, data):
        url = urljoin(self.url, "options/")
        response = requests.post(url=url, headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def update_option(self, option_id, data):
        url = urljoin(self.url, f"options/{option_id}")
        response = requests.put(url=url,headers=self.headers,data=json.dumps(data))
        return self._handle_response(response)

    def delete_option(self, option_id):
        url = urljoin(self.url, f"options/{option_id}")
        response = requests.delete(url=url, headers=self.headers)
        return self._handle_response(response)

    def list_option_combinations(self, product_id, items_per_page=None, page=None):
        params = {"product_id": product_id}
        headers={"Authorization": self.credentials}
        if items_per_page: params["items_per_page"] = items_per_page
        if page: params["page"] = page

        response = requests.get(url=self.base_url, params=params, headers=headers)
        return self._handle_response(response)

    def get_option_combination(self, combination_hash):
        url = urljoin(self.base_url, combination_hash)
        headers={"Authorization": self.credentials}
        response = requests.get(url=url, headers=headers)
        return self._handle_response(response)

    def create_option_combination(self, product_id, combination, amount=None, position=None):
        data = {"product_id": product_id, "combination": combination}
        headers={"Authorization": self.credentials}
        
        if amount: data["amount"] = amount
        if position: data["position"] = position
       
        response = requests.post(url=self.base_url, data=data, headers=headers)
        return self._handle_response(response)

    def update_option_combination(self, combination_hash, product_code=None, amount=None, position=None):
        data = {}
        headers={"Authorization": self.credentials}

        if product_code: data["product_code"] = product_code
        if amount: data["amount"] = amount
        if position: data["position"] = position
       
        url = urljoin(self.base_url, combination_hash)
        response = requests.put(url=url, data=data, headers=headers)
        return self._handle_response(response)

    def delete_option_combination(self, combination_hash, product_id):
        params = {"product_id": product_id}
        headers={"Authorization": self.credentials}
        url = urljoin(self.base_url, combination_hash)
        response = requests.delete(url=url, params=params, headers=headers)
        return self._handle_response(response)

    # list exceptions

    def list_exceptions(self, product_id):
        params = {"product_id": product_id}
        headers={"Authorization": self.credentials}
        response = requests.get(url=self.exceptions_url,params=params,headers=headers)
        return self._handle_response(response)

    def get_exception(self, exception_id):
        url = urljoin(self.exceptions_url, exception_id)
        headers={"Authorization": self.credentials}
        response = requests.get(url=url, headers=headers)
        return self._handle_response(response)

    def create_exception(self, product_id, combination):
        data = {"product_id": product_id, "combination": combination}
        headers={"Authorization": self.credentials}
        response = requests.post(url=self.exceptions_url, data=data, headers=headers)
        return self._handle_response(response)

    def update_exception(self, exception_id, combination):
        data = {"combination": combination}
        headers={"Authorization": self.credentials}
        url = urljoin(self.exceptions_url, exception_id)
        response = requests.put(url=url, data=data, headers=headers)
        return self._handle_response(response)

    def delete_exception(self, exception_id, product_id):
        params = {"product_id": product_id}
        headers={"Authorization": self.credentials}
        url = urljoin(self.exceptions_url, exception_id)
        response = requests.delete(url=url, params=params, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                return json_response
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(f"Request failed with status code {response.status_code}")
