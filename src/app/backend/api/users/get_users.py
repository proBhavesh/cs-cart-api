import os
import base64
import requests
import json
from dotenv import load_dotenv

# Importing the global data file to access the BASE_URL
from ..shared.global_data import BASE_URL


class UserService:
    def __init__(
        self,
        admin_email,
        admin_api_key,
        url=None,
    ):
        if not admin_email or not admin_api_key:
            raise ValueError("Admin email and API key must be set")

        self.credentials = base64.b64encode(
            f"{admin_email}:{admin_api_key}".encode()
        ).decode()

        self.url = url if url else BASE_URL
        self.users_url = self.url + "/api/users/"
        self.usergroups_url = self.url + "/api/usergroups/"

    def get_users(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(
            self.users_url,
            headers={"Authorization": f"Basic {self.credentials}"},
            params=params
        )
        return self._handle_response(response)

    def get_user(self, user_id):
        url = self.users_url + str(user_id)
        response = requests.get(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def create_user(self, user):
        response = requests.post(
            self.users_url,
            data=user,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def update_user(self, user_id, user):
        url = self.users_url + str(user_id)
        response = requests.put(
            url,
            data=user,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def delete_user(self, user_id):
        url = self.users_url + str(user_id)
        response = requests.delete(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def get_usergroups(self, page=1, items_per_page=10):
        params = {"page": page, "items_per_page": items_per_page}
        response = requests.get(
            self.usergroups_url,
            headers={"Authorization": f"Basic {self.credentials}"},
            params=params
        )
        return self._handle_response(response)

    def get_usergroup(self, group_id):
        url = self.usergroups_url + str(group_id)
        response = requests.get(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def create_usergroup(self, group):
        response = requests.post(
            self.usergroups_url,
            data=group,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def update_usergroup(self, group_id, group):
        url = self.usergroups_url + str(group_id)
        response = requests.put(
            url,
            data=group,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def delete_usergroup(self, group_id):
        url = self.usergroups_url + str(group_id)
        response = requests.delete(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def get_user_usergroups(self, user_id):
        url = self.url + f"/api/users/{user_id}/usergroups"
        response = requests.get(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def update_user_usergroup_status(self, user_id, group_id, status):
        url = self.url + f"/api/users/{user_id}/usergroups/{group_id}"
        data = {"status": status}
        response = requests.put(
            url,
            data=data,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def delete_user_from_usergroup(self, user_id, group_id):
        url = self.url + f"/api/users/{user_id}/usergroups/{group_id}"
        response = requests.delete(
            url,
            headers={"Authorization": f"Basic {self.credentials}"}
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            try:
                return response.json()
            except json.JSONDecodeError:
                print(response.text)
                raise ValueError("Response from server was not a valid JSON")
        else:
            raise ConnectionError(
                f"Request failed with status code {response.status_code}"
            )
