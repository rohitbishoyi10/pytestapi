from pydantic import BaseModel


class Hosting_Regrade_Payload_DC(BaseModel):
    url_hash: str = ''
    host_id: str = ''
    product: str = ''
    term: str = ''


class Hosting_Plan_Regrading_DC(BaseModel):
    regrading_action:str = ''
    domain_name: str = ''
    type: str = ''
    subtype_active: str = ''
    subtype_switch:str = ''
    payment_type: str = ''
    req_data: Hosting_Regrade_Payload_DC = ''