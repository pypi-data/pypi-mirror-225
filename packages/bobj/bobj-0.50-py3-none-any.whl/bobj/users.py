# Code for user module in libraray

import requests
import random
import string
from . import support as sup


class UserManagement:
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)

    def _make_request(self, method, endpoint, body=None):
        url = sup._get_url(endpoint)
        response = getattr(requests, method)(
            url, headers=self.header, json=body)
        return sup._handle_response(response)

    def list_users(self, sort=None, updated=None, name_filter=None, page=1, pagesize=50):
        # Constructing the endpoint with optional query parameters
        query_params = []
        if sort:
            query_params.append(f'sort={sort}')
        if updated:
            query_params.append(f'updated={updated}')
        if name_filter:
            query_params.append(f'name={name_filter}')
        query_params.append(f'page={page}')
        query_params.append(f'pagesize={pagesize}')
        endpoint = f'users?{"&".join(query_params)}'

        response = requests.get(sup._get_url(endpoint), headers=self.header)
        return sup._handle_response(response)



    def create_user(self, username, **kwargs):
        password = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10))
        user_attrs = {
            "password": password,
            "forcepasswordchange": "true",
            "name": username,
            **kwargs
        }

        url = self._get_url("users/user")
        user_data = sup.construct_body(**user_attrs)

        response = requests.post(url, headers=self.headers, data=user_data)

        if response.status_code == 201:
            request_details = [username, password, *kwargs.values()]
            return request_details

        return None

    def get_user_details_by_id(self, user_id):
        return self._make_request('get', f'users/{user_id}')

    def get_user_details_by_username(self, username, pagesize=50, page=1):
        user_id = self._find_user_id_by_username(username, pagesize, page)
        return None if user_id is None else self._make_request('get', f'users/{user_id}')

    def modify_user(self, user_id, user_details):
        body = sup.construct_body(**user_details)
        return self._make_request('put', f'users/{user_id}', body)

    def delete_user(self, user_id):
        return self._make_request('delete', f'users/{user_id}')

    def _find_user_id_by_username(self, username):
        # Using the exact search functionality to find the user by username
        users_page = self.list_users(name_filter=username)
        if not users_page:
            return None

        # Since the search is exact, the first matching user (if any) will have the desired username
        for user in users_page:
            if user['name'] == username:
                return user['id']

        return None
