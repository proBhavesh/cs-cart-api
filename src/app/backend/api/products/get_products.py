from calendar import day_abbr
from multiprocessing import resource_tracker
from urllib.parse import urljoin
from wsgiref.util import request_uri
import requests
import json
from typing import Any, Dict, Optional
from api import BASE_URL, encode_credentials


class ProductsService:
    def __init__(self, vendor_email: str, vendor_api_key: str):
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = urljoin(BASE_URL, "/api/products/")
        self.product_variation_groups_url = urljoin(
            BASE_URL, "/api/product_variations_groups/"
        )
        self.features_url = urljoin(BASE_URL, "/api/features/")
        self.base_url = urljoin(BASE_URL, "/api/combinations/")
        self.exceptions_url = urljoin(BASE_URL, "/api/exceptions/")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_products(self) -> Any | Dict[str, str]:
        return self._handle_request(method="GET")

    def create_product(self, payload: Dict[str, Any]) -> Any | Dict[str, int | str]:
        return self._handle_request(method="POST", json=payload)

    def update_product(
        self, product_id: int, payload: Dict[str, Any]
    ) -> Any | Dict[str, int | str]:
        url = urljoin(self.url, str(product_id))
        return self._handle_request(method="PUT", url=url, json=payload)

    def delete_product(self, product_id: int) -> Any | dict[str, str]:
        url = urljoin(self.url, str(product_id))
        return self._handle_request(url=url, method="DELETE")

    def get_product_features(self, product_id: int):
        url = urljoin(self.url, "/features/" + str(product_id))
        return self._handle_request(url=url, method="GET")

    def update_product_features(self, product_id: int, payload: Dict[str, Any]):
        url = urljoin(self.url, str(product_id))
        return self._handle_request(url=url, method="PUT", json=payload)

    def get_features(self, params={}):
        return self._handle_request(url=self.features_url, method="GET", params=params)

    def get_feature(self, feature_id):
        url = urljoin(self.features_url, str(feature_id))
        return self._handle_request(url=url, method="GET")

    def create_feature(self, feature_data):
        return self._handle_request(
            url=self.features_url, method="POST", json=feature_data
        )

    def update_feature(self, feature_id: int, feature_data: Dict[str, Any]):
        url = urljoin(self.features_url, str(feature_id))
        return self._handle_request(url=url, method="PUT", json=feature_data)

    def delete_feature(self, feature_id: int):
        url = urljoin(self.features_url, str(feature_id))
        return self._handle_request(url=url, method="DELETE")

    def get_product_variations(self, group_id):
        url = urljoin(self.url, f"?variation_group_id={group_id}")
        return self._handle_request(url=url, method="GET")

    def add_product_to_group(self, id, data: Dict):
        url = urljoin(self.url, str(id))
        return self._handle_request(url=url, method="PUT", data=data)

    def detach_product_variation(self, id):
        url = urljoin(self.url, f"{id}/detach_product_variation")
        return self._handle_request(url=url, method="POST")

    def set_default_variation(self, id):
        url = urljoin(self.url, f"{id}/set_default_product_variation")
        return self._handle_request(url=url, method="POST")

    def generate_variations(self, id, combinations):
        url = urljoin(self.url, f"{id}/generate_product_variations")
        data = {"combinations": combinations}
        return self._handle_request(url=url, method="POST", data=data)

    def create_variation_group(self, data: Dict):
        return self._handle_request(
            url=self.product_variation_groups_url, method="POST", data=data
        )

    def get_variation_groups(self):
        return self._handle_request(url=self.product_variation_groups_url, method="GET")

    def get_variation_group(self, id_or_code):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        return self._handle_request(url=url, method="GET")

    def update_variation_group(self, id_or_code, data: Dict):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        return self._handle_request(url=url, method="PUT", data=data)

    def delete_variation_group(self, id_or_code):
        url = urljoin(self.product_variation_groups_url, id_or_code)
        return self._handle_request(
            url=self.product_variation_groups_url, method="DELETE"
        )

    def list_product_options(self, product_id):
        url = urljoin(self.url, f"{product_id}/options")
        return self._handle_request(url=url, method="GET")

    def get_specific_option(self, option_id):
        url = urljoin(self.url, f"options/{option_id}")
        return self._handle_request(url=url, method="GET")

    def create_option(self, data: Dict):
        url = urljoin(self.url, "options/")
        return self._handle_request(url=url, method="POST", data=data)

    def update_option(self, option_id, data):
        url = urljoin(self.url, f"options/{option_id}")
        return self._handle_request(url=url, method="PUT", data=data)

    def delete_option(self, option_id):
        url = urljoin(self.url, f"options/{option_id}")
        return self._handle_request(url=url, method="DELETE")

    def list_option_combinations(self, product_id, items_per_page=None, page=None):
        params = {"product_id": product_id}
        headers = {"Authorization": self.credentials}
        if items_per_page:
            params["items_per_page"] = items_per_page
        if page:
            params["page"] = page

        return self._handle_request(
            url=self.base_url, method="GET", params=params, headers=headers
        )

    def get_option_combination(self, combination_hash):
        url = urljoin(self.base_url, combination_hash)
        headers = {"Authorization": self.credentials}
        return self._handle_request(url=url, method="GET", headers=headers)

    def create_option_combination(
        self, product_id, combination, amount=None, position=None
    ):
        data = {"product_id": product_id, "combination": combination}
        headers = {"Authorization": self.credentials}

        if amount:
            data["amount"] = amount
        if position:
            data["position"] = position

        return self._handle_request(
            url=self.base_url, method="POST", headers=headers, data=data
        )

    def update_option_combination(
        self, combination_hash, product_code=None, amount=None, position=None
    ):
        data = {}
        headers = {"Authorization": self.credentials}

        if product_code:
            data["product_code"] = product_code
        if amount:
            data["amount"] = amount
        if position:
            data["position"] = position

        url = urljoin(self.base_url, combination_hash)
        return self._handle_request(url=url, method="PUT", headers=headers, data=data)

    def delete_option_combination(self, combination_hash, product_id):
        params = {"product_id": product_id}
        headers = {"Authorization": self.credentials}
        url = urljoin(self.base_url, combination_hash)
        return self._handle_request(
            url=url, method="DELETE", headers=headers, params=params
        )

    # list exceptions

    def list_exceptions(self, product_id):
        params = {"product_id": product_id}
        headers = {"Authorization": self.credentials}
        return self._handle_request(
            url=self.exceptions_url, method="GET", headers=headers, params=params
        )

    def get_exception(self, exception_id):
        url = urljoin(self.exceptions_url, exception_id)
        headers = {"Authorization": self.credentials}
        return self._handle_request(url=url, method="GET", headers=headers)

    def create_exception(self, product_id, combination):
        data = {"product_id": product_id, "combination": combination}
        headers = {"Authorization": self.credentials}
        return self._handle_request(
            url=self.exceptions_url, method="POST", headers=headers, data=data
        )

    def update_exception(self, exception_id, combination):
        data = {"combination": combination}
        headers = {"Authorization": self.credentials}
        url = urljoin(self.exceptions_url, exception_id)
        return self._handle_request(url=url, method="PUT", headers=headers, data=data)

    def delete_exception(self, exception_id, product_id):
        params = {"product_id": product_id}
        headers = {"Authorization": self.credentials}
        url = urljoin(self.exceptions_url, exception_id)
        return self._handle_request(
            url=url, method="DELETE", headers=headers, params=params
        )

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
                    url=_url, headers=_headers, params=params, json=json, data=data
                )
            elif method == "POST":
                response = requests.post(
                    url=_url, headers=_headers, params=params, json=json, data=data
                )
            elif method == "PUT":
                response = requests.put(
                    url=_url, headers=_headers, params=params, json=json, data=data
                )
            elif method == "DELETE":
                response = requests.delete(
                    url=_url, headers=_headers, params=params, json=json, data=data
                )
            else:
                raise ValueError("Unsupported HTTP method")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"RequestException ({method}): {e}")
            return {"Error": str(e)}
