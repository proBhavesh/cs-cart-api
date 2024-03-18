import json
from urllib.parse import urljoin
import requests
from typing import Any, Dict, Optional

from api import BASE_URL, encode_credentials


class StoresService:
    """
    Provides methods for interacting with the Stores API endpoints of CS-Cart.
    Includes functionality to list, retrieve, create, update, and delete stores,
    as well as manage shipping methods.

    Attributes:
        credentials (str): Encoded credentials for Basic Authentication.
        url (str): Base URL for stores endpoint.
        shipping_url (str): Base URL for shipping methods endpoint.
        headers (dict): Headers for API requests, including Authorization.
    """

    def __init__(self, store_email: str, store_api_key: str):
        """
        Initializes the service with the provided store email and API key.

        Args:
            store_email (str): Email of the store admin user.
            store_api_key (str): API key for the store's admin account.

        Raises:
            ValueError: If store email or API key is missing.
        """
        if not store_email or not store_api_key:
            raise ValueError("Store email and API key must be set")

        self.credentials = encode_credentials(store_email, store_api_key)
        self.url = urljoin(BASE_URL, "/api/stores/")
        self.shipping_url = urljoin(BASE_URL, "/api/shippings/")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_stores(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        """
        Retrieves a list of stores from the CS-Cart API.

        Args:
            params (Optional[Dict]): Parameters to filter and paginate the stores list.

        Returns:
            Any | Dict[str, str]: Response from the API with a dictionary of stores data.
        """
        return self._handle_request(method="GET", params=params)

    def get_store(self, store_id: int) -> Any | Dict[str, str]:
        """
        Retrieves details of a specific store by its ID.

        Args:
            store_id (int): The unique identifier of the store.

        Returns:
            Any | Dict[str, str]: Response from the API with details of the store.
        """
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="GET")

    def create_store(self, store_data: Dict[str, Any]) -> Any | Dict[str, str]:
        """
        Creates a new store in the CS-Cart store.

        Args:
            store_data (Dict[str, Any]): Data for the new store.

        Returns:
            Any | Dict[str, str]: Response from the API after creating the store.
        """
        return self._handle_request(method="POST", json=store_data)

    def update_store(
        self, store_id: int, store_data: Dict[str, Any]
    ) -> Any | Dict[str, str]:
        """
        Updates an existing store by its ID.

        Args:
            store_id (int): The unique identifier of the store to update.
            store_data (Dict[str, Any]): Data to update the store with.

        Returns:
            Any | Dict[str, str]: Response from the API after updating the store.
        """
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="PUT", json=store_data)

    def delete_store(self, store_id: int) -> int | Dict[str, str]:
        """
        Deletes a store by its ID.

        Args:
            store_id (int): The unique identifier of the store to delete.

        Returns:
            int | Dict[str, str]: Response from the API, typically the status code.
        """
        url = urljoin(self.url, str(store_id))
        return self._handle_request(url=url, method="DELETE")

    def get_shipping_methods(
        self, params: Optional[Dict] = None
    ) -> Any | Dict[str, str]:
        """
        Retrieves a list of shipping methods from the CS-Cart API.

        Args:
            params (Optional[Dict]): Parameters to filter and paginate the shipping methods list.

        Returns:
            Any | Dict[str, str]: Response from the API with a dictionary of shipping methods data.
        """
        return self._handle_request(url=self.shipping_url, method="GET", params=params)

    def get_shipping_method(self, shipping_id: int) -> Any | Dict[str, str]:
        """
               Retrieves details of a specific shipping method by its ID.

               Args:
                   shipping_id (int): The unique identifier of the shipping method.

               Returns:
                   Any

        | Dict[str, str]: Response from the API with details of the shipping method.
        """
        url = urljoin(self.shipping_url, str(shipping_id))
        return self._handle_request(url=url, method="GET")

    def create_shipping_method(
        self, shipping_data: Dict[str, Any]
    ) -> Any | Dict[str, str]:
        """
        Creates a new shipping method in the CS-Cart store.

        Args:
            shipping_data (Dict[str, Any]): Data for the new shipping method.

        Returns:
            Any | Dict[str, str]: Response from the API after creating the shipping method.
        """
        return self._handle_request(
            url=self.shipping_url, method="POST", json=shipping_data
        )

    def update_shipping_method(
        self, shipping_id: int, shipping_data: Dict[str, Any]
    ) -> Any | Dict[str, str]:
        """
        Updates an existing shipping method by its ID.

        Args:
            shipping_id (int): The unique identifier of the shipping method to update.
            shipping_data (Dict[str, Any]): Data to update the shipping method with.

        Returns:
            Any | Dict[str, str]: Response from the API after updating the shipping method.
        """
        url = urljoin(self.shipping_url, str(shipping_id))
        return self._handle_request(url=url, method="PUT", json=shipping_data)

    def delete_shipping_method(self, shipping_id: int) -> int | Dict[str, str]:
        """
        Deletes a shipping method by its ID.

        Args:
            shipping_id (int): The unique identifier of the shipping method to delete.

        Returns:
            int | Dict[str, str]: Response from the API, typically the status code.
        """
        url = urljoin(self.shipping_url, str(shipping_id))
        return self._handle_request(url=url, method="DELETE")

    def _handle_response(self, response: Any) -> Dict:
        """
        Handles the response from an API request.

        Args:
            response (Any): The response object from the requests library.

        Returns:
            Dict: Parsed JSON data from the response.
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
        Handles making an API request to the CS-Cart server.

        Args:
            url (Optional[str]): URL for the request. Defaults to base URL.
            method (Optional[str]): HTTP method for the request.
            headers (Optional[Dict]): Custom headers for the request.
            json (Optional[Dict]): JSON data for the request body.
            data (Optional[Dict]): Form data for the request body.
            params (Optional[Dict]): URL parameters.

        Returns:
            Any | Dict[str, int | str]: Response from the API request.
        """
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
