from pydantic import BaseModel

class Update_Account_Password_Payload_DC(BaseModel):
    pw1: str = ''
    pw2: str = ''
    token: str = ''
    tos: str = 'true'

class Update_Account_Password_DC(BaseModel):
    domain_name : str = ''
    cust_id: str = ''
    set_password_response: str = ''
    payment_token: str = ''
    admin_user: str = ''
    setPwd_response: str = ''
    req_data: Update_Account_Password_Payload_DC = ''
