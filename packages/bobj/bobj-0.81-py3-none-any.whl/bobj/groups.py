import requests
from . import support as sup

class _groupmanagement:
    
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)


    def _list_groups(self, **kwargs):
        
        url = f"{self.url}/v1/usergroups"
        params = sup._fetch_kwargs(self, **kwargs)

        # Make the GET request
        response = requests.get(url, headers=self.header, params=params)
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
