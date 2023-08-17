import requests
from urllib.parse import urlparse
from . import support as sup


class _bovalidation:
    
    def __init__(self, url, **kwargs):
        
        self.url = url
        self.mode = kwargs.get('mode', None)
        self._validate_url()
        
        self.validate_kwargs(kwargs)  
        if not self._is_logon_token_valid():
            self._validate_params(**kwargs)
            self._generate_logon_token()



    def validate_kwargs(self, kwargs):  # Accepting kwargs as a parameter
        for param, value in kwargs.items():
            if param not in ['username', 'password', 'auth_type', 'prompt', 'mode']:                
                sup.notify(f"Invalid parameter: {param} with value: {value}. Please check the parameters again.", code="Exit")



    def _validate_url(self):
        parsed_url = urlparse(self.url)
        
        # Check if the scheme is missing a forward slash
        if parsed_url.scheme and not parsed_url.netloc:
            sup.notify(f"{parsed_url.scheme} passed seem to be have some issue with syntax. Please correct the URL.", code="Exit")
            return False
        
        if parsed_url.scheme and parsed_url.netloc:
            return True  # URL is valid
    
        # Check with "https" and "http" prefixes
        for scheme in ['https', 'http']:
            modified_url = f"{scheme}://{self.url}"
            parsed_url = urlparse(modified_url)
            if parsed_url.scheme and parsed_url.netloc:
                sup.notify(f"The URL works with '{scheme}' prefix. Please include the correct prefix.", code="Exit")
                return True
    
        sup.notify("Invalid URL. Please check the URL again.", code=1)
        return False



    def _is_logon_token_valid(self):
        
        print("Checking if logon_token exists:", hasattr(self, 'logon_token'))
        if hasattr(self, 'logon_token'):
            print("Value of logon_token:", self.logon_token)
                
        # Check if the logon_token attribute exists
        if not hasattr(self, 'logon_token'):
            print ("Returning False as logon token is not in object")
            return False
          
        print ("tehre is logon token in object, hence validating if it is valid")

        # Making a request to the BO server with the existing token to check its validity
        header = sup.create_header(self.logon_token)
        print ("checking if logon token is already there")
        response = requests.get(f'{self.url}/logon/long', headers=header)  # Replace with the appropriate endpoint for token validation
        print (response)
        response_json = response.json()
        
          
        # Check the response status and content to determine if the token is valid
        if response.status_code == 200:
            return True
              
        elif response.status_code == 401:  # Unauthorized
            if self.mode == 'secure':
                sup.notify("Logon token has expired. Please enter your password again.", code="TokenExpired")
                self.password = input("Enter password: ")
                self._generate_logon_token()  # Regenerate the token with the new password
            else:
                sup.notify("Logon token is invalid. Response Code: {response.status_code}", code="Error")
            return False
          
        else:
            
            sup.inform_bobj_error(response_json)
            return False

 

    def _validate_params(self, **kwargs):
        
        # Extract parameters from kwargs
        self.username = kwargs.get('username').strip() if kwargs.get('username') else None
        self.password = kwargs.get('password').strip() if kwargs.get('password') else None
        self.auth_type = kwargs.get('auth_type').strip() if kwargs.get('auth_type') else None

       
        # Check if any of the required parameters are missing
        missing_params = [param for param in ['username', 'password', 'auth_type'] if getattr(self, param) is None]
    
        # If all three are missing, prompt user to enter them
        if len(missing_params) == 3:
            sup.notify("All required parameters (username, password, auth_type) are missing. Please enter them.", code = 1)
            self.username = input("Enter username: ")
            self.password = input("Enter password: ")
            self.auth_type = input("Enter authentication type: ")
            return True
    
        # If not all three are missing, ask user to enter missing values or all values
        elif missing_params:
            choice = int(input(f"Some required parameters are missing: {', '.join(missing_params)}. Enter '0' to enter missing values or '1' to enter all values: "))
            if choice == 0:
                for param in missing_params:
                    setattr(self, param, input(f"Enter {param}: "))
            elif choice == 1:
                self.username = input("Enter username: ")
                self.password = input("Enter password: ")
                self.auth_type = input("Enter authentication type: ")
            else:
                sup.notify("Invalid choice. Please try again.", code = 1)
                return False
    
        # Check for any other kwargs and notify user
          
        return True


    def _generate_logon_token(self):
        # Endpoint to generate the logon token (replace with the actual endpoint as per the BO server's API documentation)
        endpoint = f'{self.url}/logon/long'

        
        payload = f'''
                    <attrs>
                        <attr name="userName" type="string">{self.username}</attr>
                        <attr name="password" type="string">{self.password}</attr>
                        <attr name="auth" type="string">{self.auth_type}</attr>
                    </attrs>
                    '''.strip()
                    
        headers = {
                       'Content-Type': 'application/xml',
                       'Accept': 'application/json',
                   }
        

    
        response = requests.post(endpoint, data=payload, headers=headers)
        
        # Checking the response status code and content to determine if the token generation was successful
        if response.status_code == 200:
                        
            self.logon_token = response.headers['X-SAP-LogonToken']
            if self.mode == 'secure':
                del self.password
            return True


        else:
            
            sup.inform_bobj_error(response)
            return False
