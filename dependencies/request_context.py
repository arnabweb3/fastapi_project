from fastapi import Header

def get_request_context(x_client_id : str  = Header(default=None)):
    return  x_client_id
    
