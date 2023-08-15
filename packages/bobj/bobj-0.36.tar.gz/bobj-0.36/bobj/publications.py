import requests
from . import support as sup

class _publications:

    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token

    def _list_publication(self, **kwargs):

        url = f"{self.url}/v1/publications"
        params = sup._fetch_kwargs(**kwargs)
        header = sup.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params)
        if response.status_code != 200:
            sup.inform_bobj_error(response)

        # Processing the response
        
        publications_list = []
        entries = response.json().get('entry', [])
        for entry in entries:
            attrs = entry.get('content', {}).get('attrs', {})
            publication = {key: value for key, value in attrs.items()}
            publications_list.append(publication)
        
        return publications_list

