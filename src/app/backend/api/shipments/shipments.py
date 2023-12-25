import os
import base64
import requests
import json

# Importing the global data file to access the BASE_URL
from ..shared.global_data import BASE_URL  # Adjusted import statement based on project structure


class ShipmentService:
    # The URL parameter is now optional and defaults to None
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

        # If no URL is provided, it defaults to BASE_URL from the global_data file
        self.url = url if url else BASE_URL + "/api/shipments"

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
