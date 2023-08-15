import requests
from . import support as sup

class _groupmanagement:
    
    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token


    def _list_groups(self, **kwargs):
        
        url = f"{self.url}/v1/usergroups"
        params = sup._fetch_kwargs(**kwargs)
        header = sup.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params)
        if response.status_code != 200:
            sup.inform_bobj_error(response)


        groups_list = []
        entries = response.json().get('entries', [])
        for entry in entries:
            group = {
                'id': entry.get('id'),
                'cuid': entry.get('cuid'),
                'name': entry.get('name'),
                'description': entry.get('description'),
                'updated': entry.get('updated'),
            }
            groups_list.append(group)

        return groups_list
