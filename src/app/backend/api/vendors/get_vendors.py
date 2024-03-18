import json
from urllib.parse import urljoin
import requests
from typing import Any, Dict, Optional

from api import BASE_URL, encode_credentials


class VendorsService:
    """
    Provides methods for interacting with the Vendors API endpoints of Multi-Vendor.
    Includes functionality to list, retrieve, create, update, and delete vendors.

    Attributes:
        credentials (str): Encoded credentials for Basic Authentication.
        url (str): Base URL for the vendors endpoint.
        headers (dict): Headers for API requests, including Authorization.
    """

    def __init__(self, vendor_email: str, vendor_api_key: str):
        """
        Initializes the service with the provided vendor email and API key.

        Args:
            vendor_email (str): Email of the vendor user.
            vendor_api_key (str): API key for the vendor account.

        Raises:
            ValueError: If vendor email or API key is missing.
        """
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        self.url = urljoin(BASE_URL, "/api/vendors/")
        self.credentials = encode_credentials(vendor_email, vendor_api_key)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

    def get_vendors(self, params: Optional[Dict] = None) -> Any | Dict[str, str]:
        """
        Retrieves a list of vendors from the Multi-Vendor API.

        Args:
            params (Optional[Dict]): Parameters to filter and paginate the vendors list.

        Returns:
            Any | Dict[str, str]: Response from the API with a dictionary of vendors data.
        """
        return self._handle_request(method="GET", params=params)

    def get_vendor(self, vendor_id: int) -> Any | Dict[str, str]:
        """
        Retrieves details of a specific vendor by their ID.

        Args:
            vendor_id (int): The unique identifier of the vendor.

        Returns:
            Any | Dict[str, str]: Response from the API with details of the vendor.
        """
        url = urljoin(self.url, str(vendor_id))
        return self._handle_request(url=url, method="GET")

    def create_vendor(self, vendor_data: Dict) -> Any | Dict[str, str]:
        """
        Creates a new vendor in the Multi-Vendor store.

        Args:
            vendor_data (Dict): Data for the new vendor.

        Returns:
            Any | Dict[str, str]: Response from the API after creating the vendor.
        """
        return self._handle_request(method="POST", json=vendor_data)

    def update_vendor(self, vendor_id: int, vendor_data: Dict) -> Any | Dict[str, str]:
        """
        Updates an existing vendor by their ID.

        Args:
            vendor_id (int): The unique identifier of the vendor to update.
            vendor_data (Dict): Data to update the vendor with.

        Returns:
            Any | Dict[str, str]: Response from the API after updating the vendor.
        """
        url = urljoin(self.url, str(vendor_id))
        return self._handle_request(url=url, method="PUT", json=vendor_data)

    def delete_vendor(self, vendor_id: int) -> Any | Dict[str, str]:
        """
        Deletes a vendor by their ID.

        Args:
            vendor_id (int): The unique identifier of the vendor to delete.

        Returns:
            Any | Dict[str, str]: Response from the API, typically the status code.
        """
        url = urljoin(self.url, str(vendor_id))
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
               Handles making an API request to the Multi-Vendor server.

               Args:
                   url (Optional[str]): URL for the request. Defaults to base URL.
                   method (Optional[str]): HTTP method

        for the request.
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
