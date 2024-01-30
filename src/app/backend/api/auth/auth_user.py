import json
from typing import Any, Dict, Optional
import requests

from api import BASE_URL, encode_credentials

# from api.store import SessionStore TODO TODO: FILE ERROR


class AuthService:
    def __init__(
        self,
        session_store,  # TODO
        admin_email: str,
        admin_api_key: str,
        url: Optional[str] = None,
    ):
        if not admin_email or not admin_api_key or not session_store:
            raise ValueError("Admin email, API key and Session store must be set")

        self.session_store = session_store  # TODO
        self.credentials = encode_credentials(admin_email, admin_api_key)
        self.url = url if url else BASE_URL
        self.langvars_url = self.url + "/api/langvars/"
        self.languages_url = self.url + "/api/languages/"

    def send_auth_request(self, user_email) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials}",
        }
        data = {"email": user_email}

        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            return self._handle_response(user_email, response)
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

    def get_langvars(
        self, lang_code: Optional[str] = None, page: int = 1, items_per_page: int = 10
    ) -> Any:
        url = self.langvars_url + (
            f"?sl={lang_code}" if lang_code else ""
        )  # TODO: Wrong Assumption
        response = requests.get(url=url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    def get_langvar(self, name: str, lang_code: Optional[str] = None) -> Any:
        url = self.langvars_url + name + (f"?sl={lang_code}" if lang_code else "")
        response = requests.get(url=url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    def create_langvar(
        self, name: str, value, lang_code: Optional[str] = None
    ) -> Any:  # TODO: vaule arg
        url = self.langvars_url + (f"?sl={lang_code}" if lang_code else "")
        data = {"name": name, "value": value}
        response = requests.post(
            url=url, data=data, headers={"Authorization": self.credentials}
        )
        return self._handle_response(response)

    def update_langvar(
        self, name: str, value, lang_code: Optional[str] = None
    ) -> Any:  # TODO: vaule arg
        url = self.langvars_url + name + (f"?sl={lang_code}" if lang_code else "")
        data = {"value": value}
        response = requests.put(
            url=url, data=data, headers={"Authorization": self.credentials}
        )
        return self._handle_response(response)

    def delete_langvar(self, name: str) -> Any:
        url = self.langvars_url + name
        response = requests.delete(url=url, headers={"Authorization": self.credentials})
        return self._handle_response(response)

    def get_languages(self, page: int = 1, items_per_page: int = 10) -> Any:
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(
            url=self.languages_url,
            headers={
                "Authorization": self.auth_service.credentials
            },  # TODO: No Such Thing
            params=params,
        )
        return self._handle_response(response)

    def get_language(self, lang_id: int) -> Any:
        url = self.languages_url + str(lang_id)
        response = requests.get(
            url=url,
            headers={
                "Authorization": self.auth_service.credentials
            },  # TODO: No Such Thing
        )
        return self._handle_response(response)

    # TODO: Type hint require doc
    def create_language(
        self, lang_code, name, status, country_code, from_lang_code=None
    ):
        data = {
            "lang_code": lang_code,
            "name": name,
            "status": status,
            "country_code": country_code,
            "from_lang_code": from_lang_code,
        }
        response = requests.post(
            url=self.languages_url,
            data=data,
            headers={
                "Authorization": self.auth_service.credentials
            },  # TODO: NO SUCH THING
        )
        return self._handle_response(response)

    # TODO: SAME AS ABOVE
    def update_language(
        self, lang_id, lang_code, name=None, status=None, country_code=None
    ):
        data = {
            "lang_code": lang_code,
            "name": name,
            "status": status,
            "country_code": country_code,
        }
        url = self.languages_url + str(lang_id)
        response = requests.put(
            url, data=data, headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    # TODO: SAME AS ABOVE
    def delete_language(self, lang_id):
        url = self.languages_url + str(lang_id)
        response = requests.delete(
            url, headers={"Authorization": self.auth_service.credentials}
        )
        return self._handle_response(response)

    def _handle_response(self, user_email, response) -> Dict[str, Any]:
        if response.status_code in [200, 201]:
            try:
                json_response = response.json()
                self.session_store.store_session_key(user_email, json_response["key"])
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
