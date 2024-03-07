from pydantic import BaseModel

class Signup_Flow(BaseModel):
    type: str = ''
    subtype: str = ''
    domain_type: str = ''
    payment_type: str = ''
    affiliates: bool = False
    affiliates_id: str = '2666243'
    irclickid: str = 'zBnTApwgHxyLW7fwUx0Mo3QBUkEWcqQ2fwOtyU0'
    ir: str = affiliates_id + '^' + irclickid + '^-'
    tax_id: str = ''
    term: str = ''
    price_flag: bool = False
