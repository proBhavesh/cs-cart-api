import base64
import requests
import json

from ..shared.global_data import BASE_URL


class APIKeyGeneratorService:
    def __init__(self, admin_email, admin_api_key, url=None):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")
        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()
        self.url = url if url else BASE_URL + "/api/generateAPIKey"

    def generate_api_key(self, vendor_email):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        payload = json.dumps({"vendor_email": vendor_email})

        try:
            response = requests.post(self.url, headers=headers, data=payload)
            print(response)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                return json_response
                print(json_response)
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
