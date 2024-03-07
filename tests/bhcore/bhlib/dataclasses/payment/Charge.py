from pydantic import BaseModel


class Charge_Cart_Payload_DC(BaseModel):
    card_token_creator: str = ''
    card_token: str = ''
    card_token_data: str = ''
    card_token_mask: str = ''
    cc_type: str = ''
    exp_month: str = ''
    exp_year: str = ''
    session_id_3ds: str = ''
    subtotal: str = ''
    locale_subtotal: str = ''
    usd_subtotal: str = ''
    total: str = ''
    locale_total: str = ''
    usd_total: str = ''
    cart_cust_id: str = ''
    cart_md5: str = ''
    purchase: str = ''
    ldomain: str = ''
    new_cc_id: str = ''
    card_secret: str = ''
    cvv2_secret: str = ''
    cart_prefix: str = 'cart'
    paas_override_gateway_name: str = '---+Allow+PaaS+to+pick+the+best+option+---'
    test_payment_gateway: str = 'on'
    pay_choice: str = 'check'
    firstname: str = 'Yashita'
    lastname: str = 'Jain'
    email: str = 'yashita.j@endurance.com'
    address: str = 'NESCO+IT+Park+Western+Express+Highway'
    city: str = 'Mumbai'
    state: str = 'MH'
    zip: str = '400063'
    country: str = 'IN'
    checknum: str = '123456'
    account_mask: str = ''
    purchase_order: str = ''
    tax_type: str = 'india_gst'
    tax_id: str = ''
    # cpanel_term: str = ''
    # reversed_cpanel_term: str = ''
    # sitelock_term: str = ''
    # reversed_sitelock_term: str = ''
    # privacy_term: str = ''
    # reverse_privacy_term: str = ''
    customer_note: str = ''
    plan_data:dict = {}

class Charge_DC(BaseModel):
    host_id : str = ''
    domain_name: str = ''
    payment_type: str = ''
    req_data: Charge_Cart_Payload_DC = ''