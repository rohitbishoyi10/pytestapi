from pydantic import BaseModel

class Account_Regrading_Flow(BaseModel):
    regrading_action:str = ''
    domain_name: str = ''
    type: str = ''
    subtype_active: str = ''
    subtype_switch:str = ''
    payment_type: str = ''
    isLoggedin: bool = False
