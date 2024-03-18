from typing import Any, Dict
from urllib.parse import urljoin
import requests
import json

from api import BASE_URL, encode_credentials


class ShipmentService:
    """
    The ShipmentService class provides methods to interact with the Shipments API endpoints of CS-Cart.

    It allows retrieving and managing shipment information. The class supports operations such as
    listing all shipments and performing authentication requests.

    Attributes:
        credentials (str): Encoded credentials for Basic Authentication.
        url (str): Base URL for the shipments endpoint.

    Methods:
        send_auth_request(): Sends an authenticated request to retrieve shipments.
    """

    def __init__(self, vendor_email: str, vendor_api_key: str):
        """
        Initializes the ShipmentService with the provided vendor email and API key.

        Args:
            vendor_email (str): The email of the vendor accessing the CS-Cart API.
            vendor_api_key (str): The API key associated with the vendor's account.

        Raises:
            ValueError: If either vendor email or API key is not provided.
        """
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.url = urljoin(BASE_URL, "/api/shipments")

    def send_auth_request(self) -> Any | Dict[str, str]:
        """
        Sends an authenticated GET request to retrieve shipments.

        Returns:
            Any | Dict[str, str]: The response from the API. This will be a dictionary of shipment data.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            response = requests.get(url=self.url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

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
