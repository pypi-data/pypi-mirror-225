import requests
from . import support as sup

class _usermanagement:
    
    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token
    
   

    def _list_users(self, **kwargs):
        
        url = f"{self.url}/v1/users"
        params = sup._fetch_kwargs(**kwargs)
        header = sup.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params) 
        if response.status_code != 200:
            sup.inform_bobj_error(response)

            
        users_list = []
        entries = response.json().get('entries', [])
        for entry in entries:
            user = {    'id': entry.get('id'),
                        'cuid': entry.get('cuid'),
                        'name': entry.get('name'),
                        'type': entry.get('type'),
                        'description': entry.get('description'),
                        'uri': entry.get('uri'),     
                   }
            users_list.append(user)

        return users_list
