import base64
from distutils.core import setup_keywords
from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
import json

from api import BASE_URL, encode_credentials


class UserService:
    def __init__(self, admin_email: str, admin_api_key: str):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")

        self.url = BASE_URL
        self.users_url = urljoin(self.url, "/api/users/")
        self.usergroups_url = urljoin(self.url, "/api/usergroups/")
        self.credentials = encode_credentials(admin_email, admin_api_key)
        self.headers = {"Authorization": f"Basic {self.credentials}"}

    def get_users(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        return self._handle_request(url=self.users_url, method="GET", params=params)

    def get_user(self, user_id):
        url = urljoin(self.users_url, str(user_id))
        return self._handle_request(url=url, method="GET")

    def create_user(self, user):
        return self._handle_request(url=self.users_url, method="POST", data=user)

    def update_user(self, user_id, user):
        url = urljoin(self.users_url, str(user_id))
        return self._handle_request(url=url, method="PUT", data=user)

    def delete_user(self, user_id):
        url = urljoin(self.users_url, str(user_id))
        return self._handle_request(url=url, method="DELETE")

    def get_usergroups(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        return self._handle_request(
            url=self.usergroups_url, method="GET", params=params
        )

    def get_usergroup(self, group_id):
        url = urljoin(self.usergroups_url, str(group_id))
        return self._handle_request(url=url, method="GET")

    def create_usergroup(self, group):
        return self._handle_request(url=self.usergroups_url, method="POST", data=group)

    def update_usergroup(self, group_id, group):
        url = urljoin(self.usergroups_url, str(group_id))
        return self._handle_request(url=url, method="PUT", data=group)

    def delete_usergroup(self, group_id):
        url = urljoin(self.usergroups_url, str(group_id))
        return self._handle_request(url=url, method="DELETE")

    def get_user_usergroups(self, user_id):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups")
        return self._handle_request(url=url, method="GET")

    def update_user_usergroup_status(self, user_id, group_id, status):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups/{group_id}")
        data = {"status": status}
        return self._handle_request(url=url, method="PUT", data=data)

    def delete_user_from_usergroup(self, user_id, group_id):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups/{group_id}")
        return self._handle_request(url=url, method="DELETE")

    def _handle_response(self, response: Any) -> Dict:
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
