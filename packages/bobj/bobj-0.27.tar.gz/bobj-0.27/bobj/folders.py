import requests
from . import support 


class _foldermanagement:

    def _fetch_Kwargs(self, **kwargs):
        sort_by = kwargs.get('sort_by', None)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)
        filter_type = kwargs.get('filter_type', None)
        updated = kwargs.get('updated', None)

        if (page is None) != (page_size is None):
            raise ValueError("Both page and page_size must be provided together, or neither should be specified")

        return sort_by, page, page_size, filter_type, updated

    def _list_folders(self, **kwargs):
        
        sort_by, page, page_size, updated, filter_type = self._fetch_listing_Kwargs(**kwargs)
        # Constructing URL
        url = f"{self.base_url}/v1/folders"
        params = {}

        # Sorting
        if sort_by:
            params['sort'] = sort_by

        # Pagination
        if page and page_size:
            params['page'] = page
            params['pagesize'] = page_size

        # Filtering (type and updated)
        if filter_type:
            params['type'] = filter_type
        if updated:
            params['updated'] = updated

        header = support.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params)
        response_data = response.json()  # Assuming JSON response

        if response.status_code != 200:
            support.inform_bobj_error(response_data)

        folders_list = []
        entries = response_data.get('entries', [])
        for entry in entries:
            folder = {
                'id': entry.get('id'),
                'cuid': entry.get('cuid'),
                'name': entry.get('name'),
                'type': entry.get('type'),
                'description': entry.get('description'),
                'ownerid': entry.get('ownerid'),
                'updated': entry.get('updated'),
            }
            folders_list.append(folder)

        return folders_list
