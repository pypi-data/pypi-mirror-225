import requests
from . import support as sup


class _categories:

    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token

    def _list_categories(self, **kwargs):

        url = f"{self.url}/v1/categories"
        params = sup._fetch_kwargs(**kwargs)
        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/xml',
            'X-SAP-LogonToken': self.logon_token,
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            sup.inform_bobj_error(response)

        # Processing the response (Assuming response.json() is able to parse the XML response)
        categories_list = []
        entries = response.json().get('entry', [])
        for entry in entries:
            attrs = entry.get('content', {}).get('attrs', {})
            category = {
                'cuid': attrs.get('cuid'),
                'parentcuid': attrs.get('parentcuid'),
                'name': attrs.get('name'),
                'description': attrs.get('description'),
                'id': attrs.get('id'),
                'ownerid': attrs.get('ownerid'),
                'type': attrs.get('type'),
                'updated': attrs.get('updated'),
                'parentid': attrs.get('parentid'),
            }
            categories_list.append(category)

        return categories_list
