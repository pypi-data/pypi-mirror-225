

def _get_url(self, endpoint):
    return f'{self.base_url}/v1/{endpoint}'

def _handle_response(self, response):
    status_code = response.status_code
    if status_code not in [200, 201]:
        raise Exception(f"Error {status_code}: {response.text}")
    return response.json() if isinstance(response.json(), list) else [response.json()]

def create_header(logon_token):
        header = {
                    'Content-Type': 'application/xml',
                    'Accept': 'application/json',
                    'X-SAP-LogonToken': logon_token,
                }
        return header
        
    
def convert_json_to_list(response_json, key='entries'):
    return response_json.get(key, [])


def validate_user_creation_params(kwargs):
    if 'name' not in kwargs or 'password' not in kwargs:
        notify("Both username and password must be provided to create a user. Please ensure that these fields are included.", code="Exit")
        return False

    kwargs.setdefault('forcepasswordchange', "true")
    return True



def construct_body(**kwargs):
    attrs = [f'<attr name="{key}" type="string">{value}</attr>' for key, value in kwargs.items()]
    attrs_xml = '<attrs>' + ''.join(attrs) + '</attrs>'
    return f'<entry><content type="application/xml">{attrs_xml}</content></entry>'



def instance_params(self, **kwargs):
    from datetime import datetime, timedelta

    days = kwargs.get('days')
    period = kwargs.get('period', '').lower()
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    if days:
        if period or start_date or end_date:
            raise ValueError("Please provide only one of 'days', 'period', or 'start_date' and 'end_date'.")
        if not isinstance(days, int):
            raise ValueError("The 'days' parameter should be an integer.")

    if period:
        if days or start_date or end_date:
            raise ValueError("Please provide only one of 'days', 'period', or 'start_date' and 'end_date'.")
        if period not in ["week", "month", "quarter", "year", "all"]:
            raise ValueError("Invalid period value.")

    if start_date or end_date:
        if days or period:
            raise ValueError("Please provide only one of 'days', 'period', or 'start_date' and 'end_date'.")
        if not start_date or not end_date:
            raise ValueError("Both 'start_date' and 'end_date' should be provided.")

    params = {}
    if days:
        params['startDate'] = (datetime.utcnow() - timedelta(days=int(days))).strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
    elif period:
        end_date = datetime.utcnow()
        if period == "week":
            start_date = end_date - timedelta(weeks=1)
        elif period == "month":
            start_date = end_date - timedelta(weeks=4)
        elif period == "quarter":
            start_date = end_date - timedelta(weeks=13)
        elif period == "year":
            start_date = end_date - timedelta(weeks=52)
        elif period == "all":
            start_date = datetime.strptime("1/1/1900 00:00:00", "%m/%d/%Y %H:%M:%S")
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    else:
        # Assuming start_date and end_date are in the format "MM/DD/YYYY"
        if " " not in start_date:
            start_date += " 00:00:00"
        if " " not in end_date:
            end_date += " 23:59:59"
        params['startDate'] = start_date
        params['endDate'] = end_date

    return params



   
    
def _fetch_kwargs(self, **kwargs):
    
    params = {}

    sort_by = kwargs.get('sort_by', None)
    page = kwargs.get('page', None)
    page_size = kwargs.get('page_size', None)
    
    if (page is None) != (page_size is None):
        raise ValueError("Both page and page_size must be provided together, or neither should be specified")

    if sort_by:
        params['sort'] = sort_by
        
    # Pagination
    if page and page_size:
        params['page'] = page
        params['pagesize'] = page_size
        
    return params 



    
    
    
        
def notify(message, code):
    
    message = f"Notification: {message}"
    print (message)
           
    if code == "Exit" :
        raise SystemExit
        
    elif code == "valueError" :
        raise ValueError
        
        
        
        
        
def inform_bobj_error(response_data):
    notify(response_data['message'], code="Exit")
    
    