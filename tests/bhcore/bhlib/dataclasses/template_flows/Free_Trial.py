from pydantic import BaseModel


#@dataclass()
class Free_Trial(BaseModel):
    type: str = ''
    subtype: str = ''
    domain_type: str = ''
    payment_type: str = ''
    affiliates: bool = False
    tax_id: str = ''
    term: str = ''
    price_flag: bool = False
