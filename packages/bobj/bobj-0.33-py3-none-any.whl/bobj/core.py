
import requests
from . import login
from . import users
from . import folders
from . import groups


class validate:
    def __init__(self, url, **kwargs):
        self._session = requests.Session()
        
        self.login = login._bovalidation(url, **kwargs)
        self.user_management = users._usermanagement(self.login)  
        self.folders_management = folders._foldermanagement(self.login)
        self.group_management = groups._groupmanagement(self.login)

        # Create other class instances and pass kwargs...
        
        
                
        def _generate_methods(self):
            method_sources = {
                "list_users": (self.user_management, "_list_users"),
                "list_folders": (self.folders_management, "_list_folders"),
                "list_groups": (self.group_management, "_list_groups"),

            }
        
            for public_name, (source, private_name) in method_sources.items():
                setattr(self, public_name, getattr(source, private_name))
          
            
      
        
      
        
      
        
      
        
      
        
      
        
      
        
      
        

    # def list_users(self, **kwargs):
    #     return self.user_management._list_users(**kwargs)
    
    # def list_groups(self, **kwargs):
    #     return self.group_management._list_groups(**kwargs)
    
    # def list_folders(self, **kwargs):
    #     return self.folders_management._list_folders()(**kwargs)
       


