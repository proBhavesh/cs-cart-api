from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
import json

from api import BASE_URL, encode_credentials


class OrdersService:
    """
    The OrdersService class provides methods to interact with the Orders API endpoints of CS-Cart.

    It offers methods to list all orders, retrieve details of a specific order, create, update, and delete orders.
    It utilizes the RESTful interface of the CS-Cart API.

    Attributes:
        credentials (str): Encoded credentials for Basic Authentication.
        url (str): Base URL for orders endpoint.
        headers (dict): Headers for the API requests, including Authorization.

    Methods:
        get_orders(params): Retrieve a list of orders.
        get_order(order_id): Retrieve details of a specific order.
        create_order(order_data): Create a new order.
        update_order(order_id, order_data): Update an existing order.
        delete_order(order_id): Delete an order.
    """

    def __init__(self, email: str, api_key: str):
        """
        Initializes the OrdersService with the provided email and API key.

        Args:
            email (str): The email of the user accessing the CS-Cart API.
            api_key (str): The API key associated with the user's account.

        Raises:
            ValueError: If either email or API key is not provided.
        """
        if not email or not api_key:
            raise ValueError("Email and API key must be set")

        self.credentials = encode_credentials(email, api_key)
        self.url = urljoin(BASE_URL, "/api/orders/")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_orders(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        """
        Retrieves a list of orders from the CS-Cart API.

        Args:
            params (Optional[Dict]): Parameters to filter and paginate the orders list.

        Returns:
            Any | Dict[str, str]: The response from the API. This will be a dictionary of order data.
        """
        return self._handle_request(method="GET", params=params)

    def get_order(self, order_id: int) -> Any | Dict[str, str]:
        """
        Retrieves details of a specific order by its ID.

        Args:
            order_id (int): The unique identifier of the order.

        Returns:
            Any | Dict[str, str]: The response from the API containing the details of the order.
        """
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="GET")

    def create_order(self, order_data: Dict[str, Any]) -> Any | Dict[str, str]:
        """
        Creates a new order in the CS-Cart store.

        Args:
            order_data (Dict[str, Any]): Data for the new order.

        Returns:
            Any | Dict[str, str]: The response from the API after creating the order.
        """
        return self._handle_request(method="POST", json=order_data)

    def update_order(
        self, order_id: int, order_data: Dict[str, Any]
    ) -> Any | Dict[str, str]:
        """
        Updates an existing order by its ID.

        Args:
            order_id (int): The unique identifier of the order to update.
            order_data (Dict[str, Any]): Data to update the order with.

        Returns:
            Any | Dict[str, str]: The response from the API after updating the order.
        """
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="PUT", json=order_data)

    def delete_order(self, order_id: int) -> int | Dict[str, str]:
        """
        Deletes an order by its ID.

        Args:
            order_id (int): The unique identifier of the order to delete.

        Returns:
            int | Dict[str, str]: The response from the API, typically the status code.
        """
        url = urljoin(self.url, str(order_id))
        return self._handle_request(url=url, method="DELETE")

    def _handle_response(self, response: Any) -> Dict:
        """
        Handles the response from an API request.

        Args:
            response (Any): The response object from requests library.

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
        params: Optional[Dict] = None,
    ) -> Any | Dict[str, int | str]:
        """
        Handles making an API request to the CS-Cart server.

        Args:
            url (Optional[str]): The URL to send the request to. Defaults to the base URL for orders.
            method (Optional[str]): The HTTP method to use for the request.
            headers (Optional[Dict]): Custom headers for the request.
            json (Optional[Dict]): JSON data to send in the body of the request.
            params (Optional[Dict]): Parameters to include in the request URL.

        Returns:
            Any | Dict[str, int | str]: The response from the API request.
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
                response = requests.get(url=_url, headers=_headers, params=params)
            elif method == "POST":
                response = requests.post(url=_url, headers=_headers, json=json)
            elif method == "PUT":
                response = requests.put(url=_url, headers=_headers, json=json)
            elif method == "DELETE":
                response = requests.delete(url=_url, headers=_headers)
            else:
                raise ValueError("Unsupported HTTP method")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"RequestException ({method}): {e}")
            return {"Error": str(e)}
