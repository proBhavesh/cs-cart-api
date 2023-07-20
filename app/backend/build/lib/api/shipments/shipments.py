import os
import base64
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ShipmentService:
    def __init__(
        self,
        vendor_email,
        vendor_api_key,
        url=None,
    ):
        # Check if vendor email and API key are set
        if not vendor_email or not vendor_api_key:
            raise ValueError("Vendor email and API key must be set")

        # Encode the credentials
        self.credentials = base64.b64encode(
            f"{vendor_email}:{vendor_api_key}".encode()
        ).decode()

        # If url is not provided, load it from environment variable
        if url is None:
            url = os.getenv("BASE_URL")

        # If url is still None, raise an error
        if url is None:
            raise ValueError(
                "URL must be set either in arguments or as an environment variable"
            )

        # Append /api/products to the base URL
        self.url = url + "/api/shipments"

    def send_auth_request(self):
        # Set headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            # Send the request and handle the response
            response = requests.get(self.url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        # Check if the response is successful
        if response.status_code in [200, 201]:
            try:
                # Try to decode the JSON response
                json_response = response.json()
                return json_response

            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
