

def create_header(logon_token):
        
        header = {
            'Content-Type': 'application/xml',
            'Accept': 'application/json',
            'X-SAP-LogonToken': logon_token,
        }
        
        return header
        
        
def notify(message, code):
    
    message = ERROR_CODES.get(code, message)
    message = f"Notification: {message}"
    print (message)
           
    if code == "Exit" :
        raise SystemExit
        
    elif code == "valueError" :
        raise ValueError
        


def inform_bobj_error(response):
    
    response_data = response.json()
    bobj_error_code = response_data.get('error_code', None)
    if bobj_error_code is None:
        error_message = 'Unknown Error: errorCode key not found in response'
        
    else :
        error_message = ERROR_CODES.get(bobj_error_code, 'Unknown Error')
        
    notify(f"Error Code: {bobj_error_code}, Message: {error_message}", code="Exit")
    
    

ERROR_CODES = {
    "RWS00002": "General server error.",
    "RWS00003": "Client input error.",
    "RWS00004": "Forbidden",
    "RWS00005": "Not Found",
    "RWS00006": "Unable to create service. See server logs for details.",
    "RWS00007": "Unknown error occurred while invoking service. See server logs for details.",
    "RWS00008": "The HTTP header does not contain the X-SAP-LogonToken attribute.",
    "RWS00009": "Resource not found: {0}",
    "RWS00010": "Resource not supported for the requested object.",
    "RWS00011": "Invalid session token timeout value: {0}.",
    "RWS00012": "Info object with ID {0} not found.",
    "RWS00013": "Duplicate Object",
    "RWS00015": "No relationship named {0}.",
    "RWS00016": "The server session is not available from the PJS service bean.",
    "RWS00017": "Encode failure.",
    "RWS00018": "{0} is NULL.",
    "RWS00019": "Illegal Argument: {0}",
    "RWS00020": "Cannot serialize value of type {0}.",
    "RWS00021": "Unterminated string.",
    "RWS00022": "Malformed date: {0}.",
    "RWS00023": "Malformed time: {0}.",
    "RWS00024": "Malformed datetime: {0}.",
    "RWS00025": "Cannot deserialize value of type {0}.",
    "RWS00026": "Cannot get the attribute name. The name is either null or empty.",
    "RWS00031": "Model error.",
    "RWS00032": "No setter.",
    "RWS00033": "Getter must not have parameters: {0}.",
    "RWS00034": "Setter must have exactly one parameter: {0}.",
    "RWS00035": "Setter {0} is not of the same type as getter {1}.",
    "RWS00036": "source: {0} + destination: {1}.",
    "RWS00037": "Reference equality is not implemented.",
    "RWS00038": "This use in hash-based collections is not implemented.",
    "RWS00039": "Class {0} is not a model class.",
    "RWS00040": "property '{0}' cannot bind to two fields: {1}, and {2}.",
    "RWS00041": "Attribute '{0}' cannot bind to two get (or set) methods: {1}, and {2}.",
    "RWS00042": "Model contains at least 1 write-only attribute. name: {0}, method: {1}.",
    "RWS00043": "No accessible constructor without parameters for class {0}.",
    "RWS00044": "{0} object is null for composition property {1}.",
    "RWS00045": "Couldn't inject property '{0}' to field {1} of type {2}.",
    "RWS00046": "Property name already exists: {0}",
    "RWS00047": "GUID must not contain the path separator '/'",
    "RWS00048": "No type for class {0}",
    "RWS00049": "Empty filter.",
    "RWS00050": "Filter may not use '{0}' in conjunction with any other filter strings.",
    "RWS00051": "A duplicate {0} instance was created.",
    "RWS00052": "Cannot process the request; the request could not be processed by the server due to malformed syntax.",
    "RWS00053": "You are not authorized to perform this request.",
    "RWS00054": "Payment required.",
    "RWS00055": "Error while performing the request; the server is unable to process the request; the request should not be repeated.",
    "RWS00056": "Error while performing the request; the server is unable to find the match for the Requested URI.",
    "RWS00057": "Method not allowed; method specified in the Request-Line is not allowed for the resource identified by the Request-URI.",
    "RWS00058": "Request cannot be processed; the resource identified by the request is only capable of generating response entities which have content characteristics which is not acceptable according to the accept headers sent in the request.",
    "RWS00059": "Proxy authentication required.",
    "RWS00060": "Request timeout; request was not sent within the time the server was prepared to wait; try making the request again.",
    "RWS00061": "Request not processed; the request could not be completed due to a conflict with the current state of the resource.",
    "RWS00062": "Request not processed; the requested resource is no longer available at the server and no forwarding address is known.",
    "RWS00063": "Request not processed; request does not contain header Content-Length; try making the request by adding valid data in Content-Length header field that contains length of the message body in the request message.",
    "RWS00064": "Precondition failed.",
    "RWS00065": "Request entity too large.",
    "RWS00066": "Request-URI too long.",
    "RWS00067": "Unsupported media type.",
    "RWS00068": "Requested range not satisfiable.",
    "RWS00069": "Request failed; the server could not process the request given in an Expect request-header field or if the server is a proxy server, it is not guaranteed that the request could be processed by the next-hop server.",
    "RWS00070": "Internal server error.",
    "RWS00071": "Request not processed; the server does not support the functionality required to fulfill the request.",
    "RWS00072": "Request not processed; the server while performing as gateway or proxy, received an invalid.",
    "RWS00073": "Service unavailable.",
    "RWS00074": "Gateway timeout.",
    "RWS00075": "HTTP version not supported.",
    "RWS00076": "Logon may not proceed because a session is already associated with this request.",
    "RWS00077": "The authentication scheme you have chosen is currently not supported.",
    "RWS00078": "The credentials could not be decoded.",
    "RWS00079": "Enter a valid input.",
    "RWS00080": "Cannot bind unknown attribute {0} to method {1}."
}
