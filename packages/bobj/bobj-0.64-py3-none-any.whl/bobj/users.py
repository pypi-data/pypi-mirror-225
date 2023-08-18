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
            raise ValueError(f"Missing mandatory fields: {', '.join(missing_fields)}")
    
        # Apply default values if not provided
        kwargs.setdefault("forcepasswordchange", True)
        kwargs.setdefault("nameduser", False)
        kwargs.setdefault("passwordexpire", True)

         # Convert boolean values to "true" or "false"
        for key, value in kwargs.items():
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"
    
        # Construct XML body using string formatting
        attrs = "\n".join(
        f'<attr name="{key}" type="{type(value).__name__}">{value}</attr>' for key, value in kwargs.items())
        xml_body = f"""<entry>
         <content type="application/xml">
         <attrs>
         {attrs}
         </attrs>
         </content>
        </entry>"""
        
        return xml_body

    
    def list_users_all(self):
        url = f"{self.base_url}/v1/users"
        response = requests.get(url, headers=self.headers)
        return sup._handle_response(self, response)

    def list_user(self, page_number, page_size):
        url = f"{self.base_url}/v1/users"
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(self, response)

    def get_id_by_username(self, name_filter):
        url = f"{self.base_url}/v1/users"
        response = requests.get(url, headers=self.headers, params={'name': name_filter})
        return sup._handle_response(self, response)

    def create_user(self, **kwargs):
        user_data = self.create_user_data(**kwargs)
        url = f"{self.base_url}/v1/users/user"
        response = requests.post(url, headers=self.headers, data=user_data)
        return sup._handle_response(self, response)

    def get_user_details(self, user_id, **kwargs):
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.get(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)

    def modify_user_details(self, user_id, **kwargs):
        user_data = self.create_user_data(**kwargs)
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.put(url, headers=self.headers, json=user_data)
        return sup._handle_response(self, response)

    def delete_user(self, user_id, **kwargs):
        url = f"{self.base_url}/v1/users/{user_id}"
        response = requests.delete(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)
