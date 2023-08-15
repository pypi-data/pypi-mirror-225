
import requests
from . import login
from . import users
from . import folders
from . import groups


class validate:
    def __init__(self, url, **kwargs):
        self._session = requests.Session()
        
        self.login = login._bovalidation(url, **kwargs)
        self.users_management = users._usermanagement(self.login)  
        self.folders_management = folders._foldermanagement(self.login)
        self.groups_management = groups._groupmanagement(self.login)

        # Create other class instances and pass kwargs...
        
    
    def list_users(self, **kwargs):
        return self.users_management._list_users(**kwargs)
    
    def list_groups(self, **kwargs):
        return self.groups_management._list_groups(**kwargs)
    
    def list_folders(self, **kwargs):
        return self.folders_management._list_folders(**kwargs)
       


