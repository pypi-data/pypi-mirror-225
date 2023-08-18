import requests
from . import support as sup

class _publicationsmanagement:

    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)

    def _list_publication(self, **kwargs):

        url = f"{self.url}/v1/publications"
        params = sup._fetch_kwargs(self, **kwargs)

        # Make the GET request
        response = requests.get(url, headers=self.header, params=params)
        sup.inform_bobj_error(response)

        # Processing the response
        
        publications_list = []
        entries = response.json().get('entry', [])
        for entry in entries:
            attrs = entry.get('content', {}).get('attrs', {})
            publication = {key: value for key, value in attrs.items()}
            publications_list.append(publication)
        
        return publications_list

