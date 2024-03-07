# from typing import List

from pydantic import BaseModel
from pydantic.class_validators import List

from tests.bhcore.bhlib.utils.Enum import *

Payment_Methods = Enum(["check", "worldpay", "payubiz"])

class Check_Payload_DC(BaseModel):
    session_id_3ds: str = ''
    access_token: str = ''
    brand: str = 'bluehost_in_dev_devees'
    c: str = ''
    card_secret: str = ''
    card_token: str = ''
    card_token_creator: str = ''
    card_token_data: str = ''
    card_token_mask: str = ''
    cc_id: str = ''
    cc_type: str = ''
    continue_anyway: str = ''
    currency: str = ''
    cust_id: str = ''
    cvv2_secret: str = ''
    data: str = ''
    domain: str = ''
    domain_action: str = ''
    ir: str = ''
    sso_provider: str = ''
    sso_token: str = ''
    sso_username: str = ''
    sug_id: str = ''
    tax_estimate: str = ''
    tax_json: str = ''
    is_test_account: str = '1'
    ctct_test_account: str = '1'
    test_self_destruct: str = '0.04'
    auto_fill_drop: str = '41xxxxxxxxxx1111 Approved'
    experience: str = 'bluerock'
    stockcpanel: str = 'stock'
    paas_override_gateway_name: str = '--- Allow PaaS to pick the best option ---'
    sku: str = ''
    firstname: str = 'Trilokesh'
    lastname: str = 'Barua'
    company: str = 'Testing: Trilokesh.b Inc'
    country: str = 'IN'
    address: str = 'NESCO IT Park, Western Express Highway'
    city: str = 'Mumbai'
    state: str = 'MH'
    zip: str = '400063'
    phone_cc: str = '91'
    phone: str = '18004194426'
    phone_ext: str = '0'
    email: str = 'svcbluehostapac@endurance.com'
    tax_type: str = 'india_gst'
    tax_id: str = ''
    term: str = ''
    privacy: str = None
    codeguard_basic: str = None
    marketgoo_start: str = None
    sitelock_essential: str = None
    office365_business_essentials: str = None
    bd_test: str = '1'
    paymethod: str = ''
    check_number: str = '123456'
    purchase_order: str = ''
    tos_agree: str = 'yes'
    no_cookie_brick: str = None
    flow: str = None

class Payment_DC(BaseModel):
    domain_action: str = 'register'
    Hosting_Type: str = ''
    Subtype: str = ''
    cust_id: str = ''
    plan: str = ''
    term: str = ''
    domain_name: str = ''
    admin_token: str = ''
    data_val: str = ''
    payment_type: str = 'credit_card'
    payment_token: str = ''
    payment_response: str = ''
    cust_id_cpanel:str = None
    # dataLayer:json =
    # payment_type: Enum = Payment_Methods.__getattr__('check')
    req_data: Check_Payload_DC = ''

class Tax_User_Info(BaseModel):
    country: str = ''
    city: str = ''
    zip: str = ''
    address: str = ''
    state: str = ''
    cust_id: str = ''
    lastname: str = ''
    currency: str = ''

class Taxable_Products(BaseModel):
    sku: str = ''
    term: str = ''

class Tax_EST_DC(BaseModel):
    user_info: Tax_User_Info = ''
    products: List[Taxable_Products] = []

