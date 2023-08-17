import requests
from . import support as sup

class _usermanagement:
    
    def __init__(self, R):
        self.base_url = R.url
        self.headers = sup.create_header(R.logon_token)
   
    def create_user_data(self, **kwargs):
        # List of mandatory fields
        mandatory_fields = ["password", "name"]
    
        # Check if any mandatory field is missing
        missing_fields = [field for field in mandatory_fields if field not in kwargs]
        if missing_fields:
            print("Missing mandatory fields:", ", ".join(missing_fields))
            return None
    
        # Add optional fields with default values if not provided
        user_data = {
            "forcepasswordchange": True,
            "nameduser": False,
            "description": "",
            "fullname": "",
            "email": "",
            "passwordexpire": False,
            **kwargs  # This will override the default values with provided values
        }
    
        return user_data
    
    def _list_users_all(self):
        url = f"{self.base_url}/v1/users"
        response = requests.get(url, headers=self.headers)
        return sup._handle_response(self, response)

    def _list_user(self, page_number, page_size):
        url = f"{self.base_url}/v1/users"
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(self, response)

    def _get_id_by_username(self, name_filter):
        url = f"{self.base_url}/v1/users"
        response = requests.get(url, headers=self.headers, params={'name': name_filter})
        return sup._handle_response(self, response)

    def _create_user(self, **kwargs):
        user_data = self.create_user_data(**kwargs)
        if user_data is None:
            raise Exception ("User creation failed due to missing mandatory fields.")
            
        url = f"{self.base_url}/v1/users/user"
        response = requests.post(url, headers=self.headers, json=user_data)
        return sup._handle_response(self, response)

    def _get_user_details(self, user_id, **kwargs):
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.get(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)

    def _modify_user_details(self, user_id, **kwargs):
        user_data = self.create_user_data(**kwargs)
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.put(url, headers=self.headers, json=user_data)
        return sup._handle_response(self, response)

    def _delete_user(self, user_id, **kwargs):
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.delete(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)
