import requests
from . import support as sup

class _foldermanagement:
    
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)


    def _get_subfolders(self, folder_id):
        subfolders = []
        subfolder_url = f"{self.url}/v1/folders/{folder_id}/children"
        subfolder_response = requests.get(subfolder_url, headers=self.headers)
        if subfolder_response.status_code == 200:
            subfolder_entries = subfolder_response.json().get('entry', [])
            for subentry in subfolder_entries:
                attrs = subentry.get('content', {}).get('attrs', {})
                subfolder = {
                    'cuid': attrs.get('cuid'),
                    'name': attrs.get('name'),
                    'description': attrs.get('description'),
                    'id': attrs.get('id'),
                    'type': attrs.get('type'),
                    'ownerid': attrs.get('ownerid'),
                    'updated': attrs.get('updated'),
                }
                subfolder['subfolders'] = self._get_subfolders(subfolder['id'], self.headers) 
                subfolders.append(subfolder)
        return subfolders

    
    def _list_folders(self):
        
        url = f"{self.url}/v1/folders"

        # Make the GET request
        response = requests.get(url, headers=self.header)
        
        print (response.status_code)
        if response.status_code != 200:
            print ("There is some error")
            sup.inform_bobj_error(response)

        # Processing the response
        folders_list = []
        entries = response.json().get('entry', [])
        for entry in entries:
            attrs = entry.get('content', {}).get('attrs', {})
            folder = {
                'cuid': attrs.get('cuid'),
                'name': attrs.get('name'),
                'description': attrs.get('description'),
                'id': attrs.get('id'),
                'type': attrs.get('type'),
                'ownerid': attrs.get('ownerid'),
                'updated': attrs.get('updated'),
            }
            folder['subfolders'] = self._get_subfolders(folder['id']) # Fetch subfolders
            folders_list.append(folder)

        return folders_list




# import requests
# from . import support as sup


# class _foldermanagement:

#     def __init__(self, login_instance):
#         self.url = login_instance.url
#         self.logon_token = login_instance.logon_token
        
        
   
    

#     def _list_folders(self, **kwargs):
        
#         url = f"{self.url}/v1/folders"
#         params = sup._fetch_kwargs(**kwargs)
#         header = sup.create_header(self.logon_token)

#         # Make the GET request
#         response = requests.get(url, headers=header, params=params)
#         if response.status_code != 200:
#             sup.inform_bobj_error(response)

#         folders_list = []
#         entries = response.json().get('entries', [])
#         for entry in entries:
#             folder = {
#                 'id': entry.get('id'),
#                 'cuid': entry.get('cuid'),
#                 'name': entry.get('name'),
#                 'type': entry.get('type'),
#                 'description': entry.get('description'),
#                 'ownerid': entry.get('ownerid'),
#                 'updated': entry.get('updated'),
#             }
#             folders_list.append(folder)

#         return folders_list
