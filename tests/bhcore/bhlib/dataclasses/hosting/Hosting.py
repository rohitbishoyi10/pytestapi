from pydantic import BaseModel


class Hosting_Payload_DC(BaseModel):
    domain_action: str = ''
    currency: str = ''
    ir: str = ''
    c: str = ''
    sku: str = ''
    show_header: str = ''
    domain: str = ''
    tld: str = 'com'
    no_cookie_brick: str = None
    flow: str = None


class Hosting_DC(BaseModel):
    Hosting_Type: str = ''
    Subtype: str = ''
    domain_name: str = ''
    cust_id: str = ''
    data_val: str = ''
    response_html: str = ''
    req_data: Hosting_Payload_DC = ''
