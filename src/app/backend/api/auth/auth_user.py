import os
import base64
import requests
import json
from api.store import SessionStore

# Importing the global data file to access the BASE_URL
from backend.global_data import BASE_URL


class AuthService:
    # The URL parameter is now optional and defaults to None
    def __init__(
        self,
        session_store,
        admin_email,
        admin_api_key,
        url=None,
    ):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")
        self.session_store = session_store
        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()
        # If no URL is provided, it defaults to BASE_URL from the global_data file
        self.url = url if url else BASE_URL
        self.langvars_url = self.url + "/api/langvars/"
        self.languages_url = self.url + "/api/languages/"

    def send_auth_request(self, user_email):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        data = {"email": user_email}

        try:
            response = requests.post(
                self.url, headers=headers, data=json.dumps(data))
            return self._handle_response(user_email, response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_langvars(self, lang_code=None, page=1, items_per_page=10):
        url = self.langvars_url + (f"?sl={lang_code}" if lang_code else "")
        response = requests.get(
            url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    def get_langvar(self, name, lang_code=None):
        url = self.langvars_url + name + \
            (f"?sl={lang_code}" if lang_code else "")
        response = requests.get(
            url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    def create_langvar(self, name, value, lang_code=None):
        url = self.langvars_url + (f"?sl={lang_code}" if lang_code else "")
        data = {"name": name, "value": value}
        response = requests.post(url, data=data, headers={
                                 "Authorization": self.credentials})
        return self._handle_response(response)

    def update_langvar(self, name, value, lang_code=None):
        url = self.langvars_url + name + \
            (f"?sl={lang_code}" if lang_code else "")
        data = {"value": value}
        response = requests.put(url, data=data, headers={
                                "Authorization": self.credentials})
        return self._handle_response(response)

    def delete_langvar(self, name):
        url = self.langvars_url + name
        response = requests.delete(
            url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    # Get installed languages
    def get_languages(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(
            self.languages_url,
            headers={"Authorization": self.auth_service.credentials},
            params=params
        )
        return self._handle_response(response)

    # Get specific language
    def get_language(self, lang_id):
        url = self.languages_url + str(lang_id)
        response = requests.get(
            url,
            headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    # Create a new language
    def create_language(self, lang_code, name, status, country_code, from_lang_code=None):
        data = {
            "lang_code": lang_code,
            "name": name,
            "status": status,
            "country_code": country_code,
            "from_lang_code": from_lang_code
        }
        response = requests.post(
            self.languages_url,
            data=data,
            headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    # Update an existing language
    def update_language(self, lang_id, lang_code, name=None, status=None, country_code=None):
        data = {"lang_code": lang_code, "name": name,
                "status": status, "country_code": country_code}
        url = self.languages_url + str(lang_id)
        response = requests.put(
            url,
            data=data,
            headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    # Delete a language
    def delete_language(self, lang_id):
        url = self.languages_url + str(lang_id)
        response = requests.delete(
            url,
            headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    def _handle_response(self, user_email, response):
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                self.session_store.store_session_key(
                    user_email, json_response["key"])
                return {
                    "Session Key": json_response["key"],
                    "Authentication Link": json_response["link"],
                }
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
