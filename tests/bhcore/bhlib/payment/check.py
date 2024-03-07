
import allure, re

from tests.bhcore.bhlib.utils.testsetup import *
from tests.bhcore.bhlib.utils.html_util import *
from bs4 import BeautifulSoup



class check():
    signup_path = '/web-hosting/signup'
    tax_path = '/api/tax_estimate'
    my_cart_path = '/hosting/cart/charge'

    acceptable_resp_text = 'Your purchase was a success!'
    acceptable_invoice_text = 'Thank you for your purchase!'
    default_products_category_list_domain_register = ['privacy', 'voucher', 'registration', 'cpanel', 'sitelock']
    default_products_category_list_domain_transfer = ['cpanel', 'sitelock']
    default_products_category_list_domain_domainless = ['cpanel', 'sitelock']

    def __init__(self, testsetup):
        self.testsetupObj = testsetup
        self.payment_Details_dict = copy.deepcopy(testsetup.test_setup_dict)

    @allure.step('Payment Method using Check')
    def pay_by_check(self, Paymentdc_obj):
        print("**********\nPaying by check\n*************")

        # tax_json = self.get_tax_json(Paymentdc_obj.cust_id, self.testsetupObj.local)
        # tax_json_dict = json.loads(tax_json)
        cookies = self.testsetupObj.getCookies()

        self.testsetupObj.setHeaders(
            {'Content-Type': 'application/x-www-form-urlencoded',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Upgrade-Insecure-Requests': '1',
             'DNT': '1',
             # 'Host': 'www.devees.alpha.bluehost.in',
             # 'Origin': 'https://www.devees.alpha.bluehost.in',
             'Pragma': 'no-cache',
             # 'Referer': 'https://www.devees.alpha.bluehost.in/web-hosting/signup',
             'Cache-Control': 'no-cache',
             'Accept-Encoding': 'gzip, deflate, br',
             })
        headers = self.testsetupObj.getHeaders()
        print('***********')
        print(headers)
        print(cookies)
        print('***********')
        # payment_data = Paymentdc_obj.req_data
        data = Paymentdc_obj.dict(exclude_none=True)
        data = self.update_addons_keys(data)

        print("Payment Data : \n" + str(data))
        response = self.testsetupObj.target.post(self.signup_path, headers=headers, cookies=cookies, data=data,
                                                 verify=self.testsetupObj.test_setup_dict['verify_ssl'])


        try:
            exp_str = self.acceptable_resp_text
            if response.assert_2xx() and data['tax_id'] == '':
                response.assert_in_body(exp_str)
                text = response.text
                href = html_find_href(text, "auth?token=")
                cust_id_cpanel = str(get_domain_custid_from_response(text))
                payment_token = find_token(href)
                payment_response = response.text
                print("Payment token " + str(payment_token))
                return payment_token, cust_id_cpanel, payment_response
            else:
                return '', '', response.text


        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error)+ str(response.text))








    def check_for_invalid_gst_in(self, data, txt):
        if data['tax_id']:
            if self.in_gst_invalid_msg in txt:
                return True
        else:
            return False

    # ***************************************     Temp Methods  ****************************************

    def update_addons_keys(self, data):
        if 'codeguard_basic' in data.keys():
            data['codeguard:basic'] = data['codeguard_basic']
            data.pop('codeguard_basic')
        if 'marketgoo_start' in data.keys():
            data['marketgoo:start'] = data['marketgoo_start']
            data.pop('marketgoo_start')
        if 'sitelock_essential' in data.keys():
            data['sitelock:essential'] = data['sitelock_essential']
            data.pop('sitelock_essential')
        if 'office365_business_essentials' in data.keys():
            data['office365:business_essentials'] = data['office365_business_essentials']
            data.pop('office365_business_essentials')
        return data