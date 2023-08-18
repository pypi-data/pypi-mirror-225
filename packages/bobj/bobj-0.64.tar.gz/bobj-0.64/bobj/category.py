import requests
from . import support as sup


class _categories:

    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)

    def _list_categories(self, **kwargs):

        url = f"{self.url}/v1/categories"
        params = sup._fetch_kwargs(self, **kwargs)
       
        # Make the GET request
        response = requests.get(url, headers=self.headers, params=params)
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
