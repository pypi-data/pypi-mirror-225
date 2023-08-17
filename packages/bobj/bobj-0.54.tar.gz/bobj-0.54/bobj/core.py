
import requests
from . import login, users, folders, groups, instances, publications



class validate:
    def __init__(self, url, **kwargs):
        self._session = requests.Session()
        
        self.login = login._bovalidation(url, **kwargs)
        self.users_management = users._usermanagement(self.login)  
        self.folders_management = folders._foldermanagement(self.login)
        self.groups_management = groups._groupmanagement(self.login)
        self.instances_management = instances._instancesmanagement(self.login)
        self.publication_management = publications._publicationsmanagement(self.login)

        # Create other class instances and pass kwargs...
        
    
    def list_users(self, **kwargs):
        return self.users_management._list_users(**kwargs)
    
    def create_users(self, **kwargs):
        return self.users_management._list_users(**kwargs)
    
    def list_groups(self, **kwargs):
        return self.groups_management._list_groups(**kwargs)
    
    def list_folders(self, **kwargs):
        return self.folders_management._list_folders(**kwargs)
    
    def job_count(self, **kwargs):
        return self.instances_management._job_count(**kwargs)
    
    def list_jobs(self, **kwargs):
        return self.instances_management._list_jobs(**kwargs)
    
    def list_publications(self, **kwargs):
        return self.publication_management._list_publication(**kwargs)
       


