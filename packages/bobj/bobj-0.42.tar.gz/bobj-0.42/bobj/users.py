import requests
from . import support as sup

class _usermanagement:
    
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)

    
    def _list_users(self, **kwargs):
        
        url = f"{self.url}/v1/users"
        params = sup._fetch_kwargs(self, **kwargs)

        # Make the GET request
        response = requests.get(url, headers= self.header, params=params) 
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
