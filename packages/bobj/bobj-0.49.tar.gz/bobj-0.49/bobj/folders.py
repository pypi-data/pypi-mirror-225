import requests
from . import support as sup

class _foldermanagement:
    
    def __init__(self,R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)
        self.folders = []

    def _list_folders(self, parent_folder_id=None, level="root"):
        url = f"{self.url}/v1/folders"

        if parent_folder_id:
            url += f"/{parent_folder_id}/children"
            
        response = requests.get(url, headers= self.header)
        
        if response.status_code == 200:
            entries = response.json().get("feed", {}).get("entry", [])
            for entry in entries:
                attrs = entry.get("content", {}).get("attrs", {})
                folder = {
                    "level": level,
                    "name": attrs.get("name"),
                    "cuid": attrs.get("cuid"),
                    "description": attrs.get("description"),
                    "id": attrs.get("id"),
                    "type": attrs.get("type"),
                    "ownerid": attrs.get("ownerid"),
                }
                self.folders.append(folder)
                # Recursively explore subfolders
                self._list_folders(parent_folder_id=folder["id"], level=f"{level} > level {len(level.split('>'))}")

    def get_folders(self):
        self._list_folders()
        return self.folders
