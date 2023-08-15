import requests
from . import support

class _groupmanagement:
    
    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token

    def _fetch_Kwargs(self, **kwargs):
        
        sort_by = kwargs.get('sort_by', None)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)
        updated = kwargs.get('updated', None)
        name_filter = kwargs.get('name_filter', None)

        if (page is None) != (page_size is None):
            raise ValueError("Both page and page_size must be provided together, or neither should be specified")

        return sort_by, page, page_size, updated, name_filter

    def _list_groups(self, **kwargs):
        sort_by, page, page_size, updated, name_filter = self._fetch_Kwargs(**kwargs)

        # Constructing URL
        url = f"{self.url}/v1/usergroups"
        params = {}

        # Sorting
        if sort_by:
            params['sort'] = sort_by

        # Pagination
        if page and page_size:
            params['page'] = page
            params['pagesize'] = page_size

        # Filtering (updated and name)
        if updated:
            params['updated'] = updated
        if name_filter:
            params['name'] = name_filter

        header = support.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params)
        response_data = response.json()  # Assuming JSON response

        if response.status_code != 200:
            support.inform_bobj_error(response_data)

        groups_list = []
        entries = response_data.get('entries', [])
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
