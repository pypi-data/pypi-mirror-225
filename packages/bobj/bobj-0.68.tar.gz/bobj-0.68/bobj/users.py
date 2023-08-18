import requests
from . import support as sup


# Endpoints for user management
LIST_USERS_ENDPOINT = "/v1/users"  # Get a list of users
CREATE_USER_ENDPOINT = "/v1/users/user"  # Create a new user
USER_DETAILS_ENDPOINT = "/v1/users/{user_id}"  # Get, modify or delete user details by user_id


class UserManagement :
    
    def __init__(self, R):
        self.base_url = R.url
        self.headers = sup.create_header(R.logon_token)
   
    def validate_user_data(self, **kwargs):
        mandatory_fields = ["password", "name"]
    
        missing_fields = [field for field in mandatory_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Missing mandatory fields: {', '.join(missing_fields)}")
    
        kwargs.setdefault("forcepasswordchange", True)
        kwargs.setdefault("nameduser", False)
        kwargs.setdefault("passwordexpire", True)
    
        for key, value in kwargs.items():
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"
        
        return kwargs

    def construct_user_data(self, **kwargs):
         # Define the XML namespace
         xmlns = "http://www.sap.com/rws/bip"
     
         # Construct attrs by considering the type as provided in the guide
         attrs = []
         for key, value in kwargs.items():
             attr_type = "string" if isinstance(value, str) else "bool"
             attrs.append('<attr name="{key}" type="{attr_type}">{value}</attr>'.format(key=key, attr_type=attr_type, value=value))
     
         # Combine attrs and create the final XML
         user_data_xml = """<entry xmlns="http://www.w3.org/2005/Atom">
                                  <content type="application/xml">
                                      <attrs xmlns="{xmlns}">
                                          {attrs}
                                      </attrs>
                                  </content>
                             </entry>""".format(xmlns=xmlns, attrs='\n'.join(attrs))
         
         return user_data_xml


    
    def list_all_users(self):
        url = self.base_url + LIST_USERS_ENDPOINT
        response = requests.get(url, headers=self.headers)
        return sup._handle_response(self, response)

    def list_users(self, page_number, page_size):
        url = self.base_url + LIST_USERS_ENDPOINT
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(self, response)

    def get_user_id_by_username(self, name_filter):
        url = self.base_url + LIST_USERS_ENDPOINT
        response = requests.get(url, headers=self.headers, params={'name': name_filter})
        return sup._handle_response(self, response)

    def create_user(self, **kwargs):
        kwargs = self.validate_user_data(**kwargs)
        user_data = self.construct_user_data(**kwargs)
        url = self.base_url + CREATE_USER_ENDPOINT
        print (user_data)
        response = requests.post(url, headers=self.headers, data=user_data)
        return sup._handle_response(self, response)

    def get_user_details(self, user_id, **kwargs):
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.get(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)
    
    
    def modify_user_details(self, user_id, **kwargs):
        kwargs = self.validate_user_data(**kwargs)
        user_data = self.construct_user_data(**kwargs)
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)
        return sup._handle_response(self, response)

  

    def delete_user(self, user_id, **kwargs):
        url = self.base_url + USER_DETAILS_ENDPOINT
        response = requests.delete(url, headers=self.headers, params=kwargs)
        return sup._handle_response(self, response)
    
    
    def reset_user_password(self, user_id, new_password):

        user_data_xml = f"""<entry>
                                 <content type="application/xml">
                                     <attrs>
                                         <attr name="password" type="string">{new_password}</attr>
                                         <attr name="forcepasswordchange" type="bool">true</attr>
                                     </attrs>
                                 </content>
                            </entry>"""
    
        url = self.base_url + USER_DETAILS_ENDPOINT
        response = requests.put(url, headers=self.headers, data=user_data_xml)
        return sup._handle_response(self, response)
        
        
    
    def find_inactive_users_by_days(self, days):
        
        from datetime import datetime, timedelta
        
        three_months_ago = datetime.now() - timedelta(days=days)
        three_months_ago_str = three_months_ago.isoformat() + "Z"
    
        url = self.base_url + LIST_USERS_ENDPOINT
        params = {'updated': f',{three_months_ago_str}'}
    
        response = requests.get(url, headers=self.headers, params=params)
    
        # Handle the response
        return sup._handle_response(self, response)
    
    def deactivate_user_by_id(self, user_id):
        
        user_data = self.construct_user_data(disabled=True)
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)    
        return sup._handle_response(self, response)


 
