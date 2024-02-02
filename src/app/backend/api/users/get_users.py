import base64
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
        self.header = {"Authorization": f"Basic {self.credentials}"}

    def get_users(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(url=self.users_url, headers=self.header, params=params)
        return self._handle_response(response)

    def get_user(self, user_id):
        url = self.users_url + str(user_id)
        response = requests.get(url=url, headers=self.header)
        return self._handle_response(response)

    def create_user(self, user):
        response = requests.post(url=self.users_url, data=user, headers=self.header)
        return self._handle_response(response)

    def update_user(self, user_id, user):
        url = urljoin(self.users_url, str(user_id))
        response = requests.put(url=url, data=user, headers=self.header)
        return self._handle_response(response)

    def delete_user(self, user_id):
        url = self.users_url + str(user_id)
        response = requests.delete(url=url, headers=self.header)
        return self._handle_response(response)

    def get_usergroups(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(
            url=self.usergroups_url, headers=self.header, params=params
        )
        return self._handle_response(response)

    def get_usergroup(self, group_id):
        url = urljoin(self.usergroups_url, str(group_id))
        response = requests.get(url, headers=self.header)
        return self._handle_response(response)

    def create_usergroup(self, group):
        response = requests.post(
            url=self.usergroups_url, data=group, headers=self.header
        )
        return self._handle_response(response)

    def update_usergroup(self, group_id, group):
        url = urljoin(self.usergroups_url, str(group_id))
        response = requests.put(url, data=group, headers=self.header)
        return self._handle_response(response)

    def delete_usergroup(self, group_id):
        url = urljoin(self.usergroups_url, str(group_id))
        response = requests.delete(url, headers=self.header)
        return self._handle_response(response)

    def get_user_usergroups(self, user_id):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups")
        response = requests.get(url, headers=self.header)
        return self._handle_response(response)

    def update_user_usergroup_status(self, user_id, group_id, status):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups/{group_id}")
        data = {"status": status}
        response = requests.put(url, data=data, headers=self.header)
        return self._handle_response(response)

    def delete_user_from_usergroup(self, user_id, group_id):
        url = urljoin(self.url, f"/api/users/{user_id}/usergroups/{group_id}")
        response = requests.delete(url, headers=self.header)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            try:
                return response.json()
            except json.JSONDecodeError:
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(f"Request failed with status code {response.status_code}")
