from pydantic import BaseModel

class My_Cluster_Login_DC(BaseModel):
    bh_account: str = ''
    bh_password: str = ''
