from pydantic import BaseModel

class MySite_Creation(BaseModel):
    type: str = ''
    domain_name: str = ''
    site_title: str = ''
    site_tagline: str = ''
    site_directory:str = None

