import requests
from . import support

class _usermanagement:
    
    def __init__(self, login_instance):
        self.url = login_instance.url
        self.logon_token = login_instance.logon_token
    
    def _fetch_Kwargs(self,**kwargs):

        sort_by = kwargs.get('sort_by', None)
        ascending = kwargs.get('ascending', True)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)
        filter_by = kwargs.get('filter_by', None)
        
        if (page is None) != (page_size is None):
            raise ValueError("Both page and page_size must be provided together, or neither should be specified")

        
        return sort_by, ascending, page, page_size, filter_by


    def _list_users(self, **kwargs):
        
        sort_by, ascending, page, page_size, filter_by = self._fetch_Kwargs(**kwargs)

        # Constructing URL
        url = f"{self.url}/v1/users"
        params = {}
        
        # Sorting
        if sort_by:
            params['sort'] = f"+{sort_by}" if ascending else f"-{sort_by}"

        # Pagination
        if page and page_size:
            params['page'] = page
            params['pagesize'] = page_size

        # Filtering (example: filtering by name)
        if filter_by:
            key, value = filter_by
            params[key] = value

        header = support.create_header(self.logon_token)

        # Make the GET request
        response = requests.get(url, headers=header, params=params)
        response_data = response.json()
        
        # In case, there is an Error 
        if 'error_code' in response_data:
            support.inform_bobj_error(response_data)
            
        users_list = []
        entries = response_data.get('entries', [])
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
