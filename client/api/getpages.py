# Import necessary libraries
import base64
import requests
import json


class GetPagesService:
    # Initialize GetPagesService class with necessary attributes
    def __init__(
        self,
        admin_email,
        admin_api_key,
        url="https://shop.migoiq.app/api/2.0/pages",
    ):
        # Check if admin_email and admin_api_key are set
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")

        # Encode credentials
        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()

        print(self.credentials)
        # self.credentials = f"{admin_email}:{admin_api_key}"
        self.url = url

    # Function to send request to get pages
    def send_pages_request(self, params=None):
        # Define headers for the request
        headers = {
            # "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }

        try:
            # Send GET request to the url with optional parameters
            response = requests.get(self.url, headers=headers, params=params)
            print(response)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    # Function to handle the response from the server
    def _handle_response(self, response):
        # Check if the status code of the response is 200
        if response.status_code == 200:
            try:
                # Convert the response to JSON
                json_response = response.json()
                return json_response
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
