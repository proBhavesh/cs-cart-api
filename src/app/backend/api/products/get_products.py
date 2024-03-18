import json
from urllib.parse import urljoin
import requests
from typing import Any, Dict, Optional
from api import BASE_URL, encode_credentials


class ProductsService:
    """
    This class provides functionalities for interacting with the products
    section of the CS-Cart/Multi-Vendor API. It includes methods to create,
    retrieve, update, and delete products, product variations, features,
    options, and combinations. It also handles exceptions related to product
    options.
    """

    def __init__(self, vendor_email: str, vendor_api_key: str):
        """
        Initializes the ProductsService with credentials for API access.

        Args:
            vendor_email (str): The vendor's email address.
            vendor_api_key (str): The API key associated with the vendor account.
        """
        # Ensure both email and API key are provided
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        # Encode the credentials for HTTP Basic Authentication
        self.credentials = encode_credentials(vendor_email, vendor_api_key)

        # Construct URLs for different product-related API endpoints
        self.url = urljoin(BASE_URL, "/api/products/")
        self.product_variation_groups_url = urljoin(
            BASE_URL, "/api/product_variations_groups/"
        )
        self.features_url = urljoin(BASE_URL, "/api/features/")
        self.base_url = urljoin(BASE_URL, "/api/combinations/")
        self.exceptions_url = urljoin(BASE_URL, "/api/exceptions/")

        # Common headers for all HTTP requests
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_products(self) -> Any | Dict[str, str]:
        """
        Retrieves a list of products.

        Returns:
            A dictionary representing the JSON response containing the list of products.
        """
        return self._handle_request(method="GET")

    def create_product(self, payload: Dict[str, Any]) -> Any | Dict[str, int | str]:
        """
        Creates a new product with the provided details.

        Args:
            payload (Dict[str, Any]): A dictionary containing product details.

        Returns:
            A dictionary representing the JSON response containing the created product's ID.
        """
        return self._handle_request(method="POST", json=payload)

    def update_product(
        self, product_id: int, payload: Dict[str, Any]
    ) -> Any | Dict[str, int | str]:
        """
        Updates an existing product identified by the given product ID.

        Args:
            product_id (int): The ID of the product to update.
            payload (Dict[str, Any]): A dictionary containing product details to be updated.

        Returns:
            A dictionary representing the JSON response with the updated product details.
        """
        url = urljoin(self.url, str(product_id))
        return self._handle_request(method="PUT", url=url, json=payload)

    def delete_product(self, product_id: int) -> Any | dict[str, str]:
        """
        Deletes a product identified by the given product ID.

        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            A dictionary representing the JSON response with the status of the deletion.
        """
        url = urljoin(self.url, str(product_id))
        return self._handle_request(url=url, method="DELETE")

    def get_product_features(self, product_id: int):
        """
        Retrieves features of a specific product.

        Args:
            product_id (int): The ID of the product.

        Returns:
            A dictionary representing the JSON response containing the product's features.
        """
        url = urljoin(self.url, "/features/" + str(product_id))
        return self._handle_request(url=url, method="GET")

    def update_product_features(self, product_id: int, payload: Dict[str, Any]):
        """
        Updates features for a specific product.

        Args:
            product_id (int): The ID of the product to update.
            payload (Dict[str, Any]): A dictionary containing features details to be updated.

        Returns:
            A dictionary representing the JSON response with the updated features details.
        """
        url = urljoin(self.url, str(product_id))
        return self._handle_request(url=url, method="PUT", json=payload)

    def get_features(self, params={}):
        """
        Retrieves a list of all product features.

        Args:
            params (dict, optional): Additional query parameters.

        Returns:
            A dictionary representing the JSON response containing all product features.
        """
        return self._handle_request(url=self.features_url, method="GET", params=params)

    def get_feature(self, feature_id):
        """
        Retrieves details of a specific product feature.

        Args:
            feature_id: The ID of the feature to retrieve.

        Returns:
            A dictionary representing the JSON response containing details of the feature.
        """
        url = urljoin(self.features_url, str(feature_id))
        return self._handle_request(url=url, method="GET")

    def create_feature(self, feature_data):
        """
        Creates a new product feature.

        Args:
            feature_data (dict): The data of the feature to create.

        Returns:
            A dictionary representing the JSON response of the newly created feature.
        """
        return self._handle_request(
            url=self.features_url, method="POST", json=feature_data
        )

    def update_feature(self, feature_id: int, feature_data: Dict[str, Any]):
        """
        Updates a specific product feature.

        Args:
            feature_id (int): The ID of the feature to update.
            feature_data (dict): The updated data for the feature.

        Returns:
            A dictionary representing the JSON response of the updated feature.
        """
        url = urljoin(self.features_url, str(feature_id))
        return self._handle_request(url=url, method="PUT", json=feature_data)

    def delete_feature(self, feature_id: int):
        """
        Deletes a specific product feature.

        Args:
            feature_id (int): The ID of the feature to delete.

        Returns:
            A dictionary representing the JSON response of the deletion process.
        """
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
        """
        Handles the HTTP response, converting it to a JSON dictionary.
        Captures and reports errors.

        Args:
            response (Any): The HTTP response object to handle.

        Returns:
            A dictionary representing the JSON response.
        """
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
        """
                Performs an HTTP request with the specified parameters.

                Args

        :
                    url (Optional[str]): The URL to send the request to.
                    method (Optional[str]): The HTTP method to use ('GET', 'POST', etc.).
                    headers (Optional[Dict]): Additional headers to send with the request.
                    json (Optional[Dict]): A JSON payload to send with the request.
                    data (Optional[Dict]): Data to send in the body of the request.
                    params (Optional[Dict]): Query parameters to append to the request URL.

                Returns:
                    A dictionary representing the JSON response.
        """
        # Default to class-level URL and headers if not specified
        if not url:
            url = self.url
        if not headers:
            headers = self.headers

        # Perform the appropriate HTTP request based on the method
        try:
            if method == "GET":
                response = requests.get(url=url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url=url, headers=headers, json=json, data=data)
            elif method == "PUT":
                response = requests.put(url=url, headers=headers, json=json, data=data)
            elif method == "DELETE":
                response = requests.delete(url=url, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"RequestException ({method}): {e}")
            return {"Error": str(e)}
