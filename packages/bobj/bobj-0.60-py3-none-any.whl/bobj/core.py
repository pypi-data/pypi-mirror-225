
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
        
    
    def list_user_all(self):
        return self.users_management._list_users_all()

    def list_user(self, page_number, page_size):
        return self.users_management._list_users(page_number=page_number, page_size=page_size)

    def get_id_by_username(self, name_filter):
        return self.users_management._get_id_by_username(name_filter=name_filter)

    def create_user(self, **kwargs):
        return self.users_management._create_user(**kwargs)

    def get_user_details(self, user_id, **kwargs):
        return self.users_management._get_user_details(user_id=user_id, **kwargs)

    def modify_user_details(self, user_id, **kwargs):
        return self.users_management._modify_user_details(user_id=user_id, **kwargs)

    def delete_user(self, user_id, **kwargs):
        return self.users_management._delete_user(user_id=user_id, **kwargs)



#####################################################################################################
    
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
       


