import yaml, requests, json, datetime, os, re, allure
from collections import Counter
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
from robot.api.deco import keyword

from tests.bhcore.bhlib.utils import html_util as handle
from tests.bhcore.bhlib.utils.apiritif import http as http


class payment:
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    signup_path = '/web-hosting/signup'
    tax_path = '/api/tax_estimate'
    my_cart_path = '/hosting/cart/charge'
    sku = ''
    plans = ''
    subtype = ''
    hosting_type = ''
    term = ''
    verifySSL = True
    acceptable_resp_text = 'Your purchase was a success!'
    acceptable_invoice_text = 'Thank you for your purchase!'
    default_products_category_list_domain_register = ['privacy', 'voucher', 'registration', 'cpanel', 'sitelock']
    default_products_category_list_domain_transfer = ['cpanel', 'sitelock']
    default_products_category_list_domain_domainless = ['cpanel', 'sitelock']

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, local, env):
        self.local = local
        self.env = env
        self.yaml_path = os.path.abspath(os.getcwd().split("automationRoot\\")[0] + "/automationRoot/variables/test_data.yaml")
        self.payloadSetup = payload.PayloadSetup(local, env)
        self.target = http.http.target(self.payloadSetup.get_host())
        self.mytarget = http.http.target(self.payloadSetup.get_myhost())
        self.isAlphaCheck(env)

    # ********************************************************************************************
    #                               Robot Exposed KEYWORDS
    # ********************************************************************************************

    @keyword
    @allure.step("Verify Payment Completion using Card.")
    def complete_card_payment(self, payment_Details_dict):
        self.load_test_data(self.yaml_path, payment_Details_dict['Hosting_Type'], payment_Details_dict['Subtype'])
        tax_json = self.get_tax_json(payment_Details_dict['ssh.custid'], self.local)
        tax_json_dict = json.loads(tax_json)
        card_token_details = self.get_card_token_details(self.local)
        card_token_details_dict = json.loads(card_token_details)
        session_id_3ds = ''
        if self.local == 'in':
            jwt_token = self.get_jwt_token(card_token_details_dict["clientId"])
            bin_number = card_token_details_dict["binData"]["number"]
            html = self.get_session_3ds(bin_number, jwt_token)
            session_id_3ds = handle.get_script_parameter(html)

        data = self.populate_data(session_id_3ds, card_token_details_dict, tax_json,
                                  tax_json_dict, payment_Details_dict)

        headers = self.create_headers()
        cookies = self.create_cookies(payment_Details_dict['admin_token'])
        # print('URL with path : ' + self.url)
        # print(headers)
        # print(cookies)
        # print(data)
        # status_code, payment_Details_dict['cpwc.resp'], a, b = api_handle.post_request(self.url, headers, cookies, data,
        #                                                                                self.verifySSL)
        # print(payment_Details_dict['cpwc.resp'])
        # # Check For Error, if any
        # error = self.error_check(status_code, payment_Details_dict['cpwc.resp'],
        #                          payment_Details_dict['suite.random_domain_name'])
        # if error == '':
        #     href = handle.html_find_href(payment_Details_dict['cpwc.resp'], "auth?token=")
        #     payment_Details_dict['cpwc.token'] = handle.find_token(href)
        # else:
        #     raise Exception("Unable to Purchase Domain, reason:" + error)
        #
        # -------------
        response = self.target.post(self.signup_path, headers=headers, cookies=cookies, data=data,
                                    verify=self.verifySSL)
        try:
            if response.assert_2xx() or response.assert_3xx():
                exp_str = self.acceptable_resp_text
                if response.assert_in_body(exp_str):
                    text = response.text
                    href = handle.html_find_href(text, "auth?token=")
                    payment_Details_dict['cpwc.token'] = handle.find_token(href)
                    print("cpwc.token " + str(payment_Details_dict['cpwc.token']))
                else:
                    raise Exception("Unable to Purchase Domain, reason:" + str(response.text))
        except Exception as e:
            error = e
            raise Exception("Card payment fail due to an error, reason:" + error)
        return payment_Details_dict

    @keyword
    @allure.step("Verify Payment Completion using Check.")
    def complete_check_payment(self, critical_test_dict, add_data=None, remove_data=None):
        html = critical_test_dict['cart_details']
        payloadSetup = payload.PayloadSetup(self.local, self.env)
        self.payloadSetup.setCookies(
            {'test': '1',
             'user_login': critical_test_dict['suite.random_domain_name'],
             'admin_user': critical_test_dict['my_admin_token'],
             'usession': critical_test_dict['usession']})
        cookies = self.payloadSetup.getCookies()

        payloadSetup.setHeaders(
            {'Content-Type': 'application/x-www-form-urlencoded',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Upgrade-Insecure-Requests': '1',
             'DNT': '1'
             })
        headers = payloadSetup.getHeaders()

        data = CaseInsensitiveDict([
            ('card_token', ''),
            ('card_token_data', ''),
            ('card_token_mask', ''),
            ('cc_type', ''),
            ('exp_month', ''),
            ('exp_year', ''),
            ('session_id_3ds', ''),
            ('subtotal', handle.html_get_attr_value(html, 'subtotal')),
            ('locale_subtotal', handle.html_get_attr_value(html, 'locale_subtotal')),
            ('usd_subtotal', ''),
            ('total', handle.html_get_attr_value(html, 'total')),
            ('locale_total', handle.html_get_attr_value(html, 'locale_total')),
            ('usd_total', ''),
            ('cart_cust_id', handle.html_get_attr_value(html, 'cart_cust_id')),
            ('cart_md5', handle.html_get_attr_value(html, 'cart_md5')),
            ('purchase', handle.html_get_attr_value(html, 'purchase')),
            ('ldomain', handle.html_get_attr_value(html, 'ldomain')),
            ('new_cc_id', ''),
            ('card_secret', ''),
            ('cvv2_secret', ''),
            ('cart_prefix', 'cart'),
            ('paas_override_gateway_name', '--- Allow PaaS to pick the best option ---'),
            ('test_payment_gateway', 'on'),
            ('pay_choice', 'check'),
            ('firstname', 'Gaurav'),
            ('lastname', 'Singh'),
            ('email', 'gaurav.si@endurance.com'),
            ('address', 'NESCO IT Park, Western Express Highway'),
            ('city', 'Mumbai'),
            ('state', 'MH'),
            ('zip', '400063'),
            ('country', 'IN'),
            ('purchase_order', ''),
            ('tax_id', ''),
            ('tax_type', 'india_gst'),
            ('customer_note', '')])
        self.setcart_data(data, add_data, remove_data)
        response = self.mytarget.post(self.my_cart_path, headers=headers, cookies=cookies, data=data,
                                      verify=self.verifySSL)
        try:
            exp_str = self.acceptable_invoice_text
            if response.assert_2xx() and response.assert_in_body(exp_str):
                return response.text
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error))

    @keyword
    @allure.step("Verify Payment Completion using Check - Cap Flow.")
    def complete_check_payment_cap_flow(self, payment_Details_dict, add_data=None, remove_data=None):
        self.load_test_data(self.yaml_path, payment_Details_dict['Hosting_Type'], payment_Details_dict['Subtype'])
        tax_json = self.get_tax_json(payment_Details_dict['ssh.custid'], self.local)
        tax_json_dict = json.loads(tax_json)

        payloadSetup = payload.PayloadSetup(self.local, self.env)
        self.payloadSetup.setCookies(
            {'test': '1',
             'user_login': payment_Details_dict['suite.random_domain_name'],
             'admin_user': payment_Details_dict['admin_token']})
        cookies = self.payloadSetup.getCookies()

        payloadSetup.setHeaders(
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
        headers = payloadSetup.getHeaders()
        data = {
            'session_id_3ds': '',
            'access_token': '',
            'brand': 'bluehost_in_dev_devees',
            'c': '',
            'card_secret': '',
            'card_token': '',
            'card_token_creator': '',
            'card_token_data': '',
            'card_token_mask': '',
            'cc_id': '',
            'cc_type': '',
            'continue_anyway': '',
            'currency': 'INR',
            'cust_id': payment_Details_dict['ssh.custid'],
            'cvv2_secret': '',
            'data': payment_Details_dict['ssh.data_val'],
            'domain': payment_Details_dict['suite.random_domain_name'],
            'domain_action': 'register',
            'ir': 'house^HOMEPAGEBYPASS^https://www.beta.bluehost.in/web-hosting/signup?' + self.plans,
            'sso_provider': '',
            'sso_token': '',
            'sso_username': '',
            'sug_id': '',
            'tax_estimate': tax_json_dict['tax'],
            'tax_json': tax_json,
            'is_test_account': '1',
            'ctct_test_account': '1',
            'test_self_destruct': '0.04',
            'auto_fill_drop': '41xxxxxxxxxx1111 Approved',
            'experience': 'bluerock',
            'stockcpanel': 'stock',
            'paas_override_gateway_name': '--- Allow PaaS to pick the best option ---',
            'sku': self.sku,
            'firstname': 'Trilokesh',
            'lastname': 'Barua',
            'company': 'Testing: Trilokesh.b Inc',
            'country': 'IN',
            'address': 'NESCO IT Park, Western Express Highway',
            'city': 'Mumbai',
            'state': 'MH',
            'zip': '400063',
            'phone_cc': '91',
            'phone': '18004194426',
            'phone_ext': '0',
            'email': 'trilokesh.b@endurance.com',
            'tax_type': 'india_gst',
            'tax_id': '',
            'term': self.plans.replace('_plan=', ':') + '-' + self.term,
            'privacy': 'on',
            'bd_test': '1',
            'paymethod': 'check',
            'check_number': '123456',
            'purchase_order': '',
            'tos_agree': 'yes'
        }
        if 'ecom' in self.hosting_type.lower():
            data['flow'] = 'woocommerce'
            data[
                'ir'] = 'house^HOMEPAGEBYPASS^https://www.beta.bluehost.in/web-hosting/signup?flow=woocommerce&' + self.plans
        elif 'dedicated' in self.hosting_type.lower():
            data['experience'] = 'legacy'
            data['stockcpanel'] = 'legacy'
            data['term'] = 'dedicated:' + self.subtype + '-' + self.term
        if 'Domainless' in payment_Details_dict.keys():
            if payment_Details_dict['Domainless']:
                print('Payment being done for Domainless flow...')
                data['domain_action'] = 'domainless'
                data.pop('privacy')
        elif 'existingDomain' in payment_Details_dict.keys():
            if payment_Details_dict['existingDomain']:
                print('Payment being done for Existing flow...')
                data['domain_action'] = 'transfer'
                data.pop('privacy')
        # print("Payment Data : \n" + str(data))
        response = self.target.post(self.signup_path, headers=headers, cookies=cookies, data=data,
                                    verify=self.verifySSL)
        try:
            exp_str = self.acceptable_resp_text
            if response.assert_2xx() and response.assert_in_body(exp_str):
                text = response.text
                href = handle.html_find_href(text, "auth?token=")
                payment_Details_dict['cpwc.token'] = handle.find_token(href)
                payment_Details_dict['cpwc.text'] = response.text
                print("cpwc.token " + str(payment_Details_dict['cpwc.token']))
                return payment_Details_dict

            # **********************************************************************************************************************
            # Below commented code is data layer validation for response, and is almost similar to above code block inside try block.
            # **********************************************************************************************************************
            # exp_str = self.acceptable_resp_text
            # if self.validate_product_list(response.text, data['domain_action']):
            #     if response.assert_2xx() and response.assert_in_body(exp_str):
            #         text = response.text
            #         href = handle.html_find_href(text, "auth?token=")
            #         payment_Details_dict['cpwc.token'] = handle.find_token(href)
            #         print("cpwc.token " + str(payment_Details_dict['cpwc.token']))
            #         return payment_Details_dict
            # else:
            #     print('**************\nUnable to validate Payment Page DataLayer. Please check response.\n**************\n'+str(response.text))
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error))

    # ********************************************************************************************
    #                               Helper Methods
    # ********************************************************************************************
    def isAlphaCheck(self, env):
        if 'alpha' in env.lower():
            self.verifySSL = False

    def load_test_data(self, yaml_file, hosting_type, subtype):
        with open(yaml_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.sku = data[hosting_type][subtype]['sku']
            self.plans = data[hosting_type][subtype]['plan']
            self.subtype = data[hosting_type][subtype]['subtype']
            self.hosting_type = hosting_type
            self.term = data['TERM']
        if hosting_type == 'freetrial':
            self.term = data[hosting_type][subtype]['TERM']

    def create_headers(self):
        self.payloadSetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        return self.payloadSetup.getHeaders()

    def create_cookies(self, admin_user_token):
        self.payloadSetup.setCookies({'alert-box': 'open', 'admin_user': admin_user_token})
        return self.payloadSetup.getCookies()

    def add_payment_details(self, payment_mode):
        data = {
            'is_test_account': '1',
            'ctct_test_account': '1',
            'test_self_destruct': '0.04',
            'auto_fill_drop': '41xxxxxxxxxx1111 Approved',
            'experience': 'bluerock',
            'stockcpanel': 'stock',
            'paas_override_gateway_name': '--- Allow PaaS to pick the best option ---',
            'sku': 'c85378f7',
            'firstname': 'Trilokesh',
            'lastname': 'Barua',
            'company': 'Testing: Trilokesh.b Inc',
            'country': 'IN',
            'address': 'NESCO IT Park, Western Express Highway',
            'city': 'Mumbai',
            'state': 'MH',
            'zip': '400063',
            'phone_cc': '91',
            'phone': '18004194426',
            'phone_ext': '0',
            'email': 'trilokesh.b@endurance.com',
            'tax_type': 'india_gst',
            'tax_id': '',
            'term': 'cpanel:basic-36',
            'privacy': 'on',
            'paymethod': payment_mode,
            'bd_test': '1',
            'tos_agree': 'yes'
        }
        return data

    # @keyword
    # def complete_card_payment(self, admin_user_token, cust_id, domain_name, data_val, hosting_type, subtype):
    #     self.load_test_data(self.yaml_path, hosting_type, subtype)
    #     local = self.local
    #     tax_json = self.get_tax_json(cust_id, local)
    #     print('TAX RESPONSE::')
    #     print(tax_json)
    #     tax_json_dict = json.loads(tax_json)
    #     card_token_details = self.get_card_token_details(local)
    #     card_token_details_dict = json.loads(card_token_details)
    #     session_id_3ds = ''
    #     if local == 'in':
    #         jwt_token = self.get_jwt_token(card_token_details_dict["clientId"])
    #         # bin_number = card_token_details_dict("binData", {}).get("number")
    #         bin_number = card_token_details_dict["binData"]["number"]
    #         html = self.get_session_3ds(bin_number, jwt_token)
    #         session_id_3ds = handle.get_script_parameter(html)
    #
    #     #account_data = self.add_payment_details('cc')
    #     data = self.populate_data(session_id_3ds, card_token_details_dict, cust_id, data_val, domain_name, tax_json, tax_json_dict)
    #
    #     headers = self.create_headers()
    #     cookies = self.create_cookies(admin_user_token)
    #     print(headers)
    #     print(cookies)
    #     print(data)
    #     #status_code, text, a, b = api_handle.post_request(self.url, headers, cookies, data, self.verifySSL)
    #     response = self.target.post(self.signup_path, headers=headers, cookies=cookies, data=data, verify=self.verifySSL)
    #     try:
    #         if response.assert_2xx() or response.assert_3xx():
    #             exp_str = self.acceptable_resp_text
    #             if response.assert_in_body(exp_str):
    #                 text = response.text
    #                 href = handle.html_find_href(text, "auth?token=")
    #                 token = handle.find_token(href)
    #             else:
    #                 raise Exception("Unable to Purchase Domain")
    #     except Exception as e:
    #         print(e)
    #         error = e
    #         raise Exception("Unable to Select Domain, reason:" + error)
    #
    #     # # Check For Error, if any
    #     # error = self.error_check(status_code, text, domain_name)
    #     # href = ''
    #     # token = ''
    #     # if error == '':
    #     #     href = handle.html_find_href(text, "auth?token=")
    #     #     token = handle.find_token(href)
    #     # else:
    #     #     raise Exception("Unable to Purchase Domain, reason:" + error)
    #
    #     return text, token

    def populate_data(self, session_id_3ds, card_token_details_dict, tax_json, tax_json_dict, payment_Details_dict):

        data = {
            'session_id_3ds': session_id_3ds,
            'access_token': '',
            'brand': 'bluehost_in',
            'c': '',
            'card_secret': '',
            'card_token': card_token_details_dict['id'],
            'card_token_creator': 'PaaS',
            'card_token_data': card_token_details_dict['creditCard']['data'],
            'card_token_mask': '411111******1111',
            'cc_id': '',
            'cc_type': 'VI',
            'continue_anyway': '',
            'currency': 'INR',
            'cust_id': payment_Details_dict['ssh.custid'],
            'cvv2_secret': '',
            'data': payment_Details_dict['ssh.data_val'],
            'domain': payment_Details_dict['suite.random_domain_name'],
            'domain_action': 'register',
            'exp_month': datetime.now().month,
            'exp_year': str(datetime.now().year)[2:4],
            'ir': 'house^HOMEPAGEBYPASS^https://www.beta.bluehost.in/web-hosting/signup?' + self.plans,
            'sso_provider': '',
            'sso_token': '',
            'sso_username': '',
            'sug_id': '',
            'tax_estimate': tax_json_dict['tax'],
            'tax_json': tax_json,
            'is_test_account': '1',
            'ctct_test_account': '1',
            'test_self_destruct': '0.04',
            'auto_fill_drop': '41xxxxxxxxxx1111 Approved',
            'experience': 'bluerock',
            'stockcpanel': 'stock',
            'paas_override_gateway_name': '--- Allow PaaS to pick the best option ---',
            'sku': self.sku,
            'firstname': 'Trilokesh',
            'lastname': 'Barua',
            'company': 'Testing: Trilokesh.b Inc',
            'country': 'IN',
            'address': 'NESCO IT Park, Western Express Highway',
            'city': 'Mumbai',
            'state': 'MH',
            'zip': '400063',
            'phone_cc': '91',
            'phone': '18004194426',
            'phone_ext': '0',
            'email': 'trilokesh.b@endurance.com',
            'tax_type': 'india_gst',
            'tax_id': '',
            'term': self.plans.replace('_plan=', ':') + '-' + self.term,
            'privacy': 'on',
            'paymethod': 'cc',
            'bd_test': '1',
            'tos_agree': 'yes'
        }
        if 'ecom' in self.hosting_type.lower():
            data['flow'] = 'woocommerce[p'
            data[
                'ir'] = 'house^HOMEPAGEBYPASS^https://www.beta.bluehost.in/web-hosting/signup?flow=woocommerce&' + self.plans
        elif 'dedicated' in self.hosting_type.lower():
            print('Its Dedicated...')
            data['experience'] = 'legacy'
            data['stockcpanel'] = 'legacy'
            data['term'] = 'dedicated:' + self.subtype + '-' + self.term
        if 'Domainless' in payment_Details_dict.keys():
            if payment_Details_dict['Domainless']:
                print('Payment being done for Domainless flow...')
                data['domain_action'] = 'domainless'
                data.pop('privacy')
        elif 'existingDomain' in payment_Details_dict.keys():
            if payment_Details_dict['existingDomain']:
                print('Payment being done for existing flow...')
                data['domain_action'] = 'transfer'
                data.pop('privacy')
        # print("Payment Data : \n" + str(data))
        return data

    @allure.step("Calculate and retrieve Tax Details in JSON format.")
    def get_tax_json(self, cust_id, local):
        payloadSetup = payload.PayloadSetup(self.local, self.env)
        payloadSetup.setHeaders(
            {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
             'Accept': 'application/json, text/javascript, */*; q=0.01'
             })
        headers = payloadSetup.getHeaders()

        if local == 'in':
            data = '{"user_info":{"country":"IN","city":"Mumbai","zip":"400063","address":"NESCO IT Park, ' \
                   'Western Express Highway","state":"MH","cust_id":"' + cust_id + '","lastname":"Barua",' \
                                                                                   '"currency":"INR"},"products":[{"sku":"' + self.sku + '","term":"' + self.term + '"}]} '
        elif local == 'com':
            data = '{"user_info":{"country":"US","city":"Tempe","zip":"85281","address":"1500 North Priest Drive"' \
                   ',"state":"AZ","cust_id":"' + cust_id + '","lastname":"Barua", "currency":"USD"},"products":[{' \
                                                           '"sku":"' + self.sku + '","term":"' + self.term + '"}]} '

        response = self.mytarget.post(self.tax_path, headers=headers, data=data, verify=self.verifySSL)
        if response.assert_2xx():
            return response.text
        else:
            print('Error Text...')
            print(response.text)
            raise Exception("Unable to calculate Tax, status:" + str(response.status_code))

    @allure.step("Retrieve details of Card Token.")
    def get_card_token_details(self, local):
        payloadSetup = payload.PayloadSetup(self.local, self.env)
        payloadSetup.setHeaders(
            {'Content-Type': 'application/json',
             'Accept': '*/*'})
        headers = payloadSetup.getHeaders()

        if local == 'in':
            data = '{"clientId":"401001","method":"CREDITCARD","type":"MULTI","creditCard":{' \
                   '"cardNumber":"4111111111111111",' \
                   '"cardSecureCode":"463","cardExpiration":"1220"}}'
        elif local == 'com':
            data = '{"clientId":"401001","method":"CREDITCARD","type":"MULTI","creditCard":{' \
                   '"cardNumber":"4457010000000009",' \
                   '"cardExpiration":"1220"}}'

        response = requests.post('https://securepay.l1.constantcontact.com/v1/payments/token', headers=headers,
                                 data=data, verify=self.verifySSL)
        # print(response.status_code)
        # print(response.text)
        return response.text

    @allure.step("Retrieve JWT Token.")
    def get_jwt_token(self, client_id):
        payloadSetup = payload.PayloadSetup(self.local, self.env)
        payloadSetup.setHeaders(
            {'Content-Type': 'application/json',
             'Accept': '*/*',
             'Referer': 'https://securepay.l1.constantcontact.com/payment/cc-cca.html?clientId=' + client_id
             })
        headers = payloadSetup.getHeaders()
        response = requests.get('https://securepay.l1.constantcontact.com/v1/jwt', headers=headers,
                                verify=self.verifySSL)
        # print("JWT Response:")
        # print(response.text)
        return response.text

    @allure.step("Retrieve 3DS session details.")
    def get_session_3ds(self, bin_number, jwt):
        payloadSetup = payload.PayloadSetup(self.local, self.env)
        payloadSetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        headers = payloadSetup.getHeaders()

        data = {
            'Bin': bin_number,
            'JWT': jwt
        }

        response = requests.post('https://secure-test.worldpay.com/shopper/3ds/ddc.html', headers=headers, data=data,
                                 verify=self.verifySSL)
        # print("3DS Response:")
        # print(response.text)
        return response.text

    def setcart_data(self, data, add_data=None, remove_data=None):
        if add_data is not None:
            for h in add_data:
                data.update([(h, add_data[h])])
        if remove_data is not None:
            for h in remove_data:
                data.pop(h)

    def get_dataLayer(self, html):
        data = {}
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.findAll('script'):
            if 'dataLayer' in str(tag):
                m = re.search(r"dataLayer = (.*?);", tag.string)
                if m:
                    for dic in json.loads(m.group(1)):
                        data.update(dic)
                    # print(str(data))
                    return data
        return data

    def validate_product_list(self, html, registration_flow):
        dataLayer = self.get_dataLayer(html)
        product_list = dataLayer['ecommerce']['purchase']['products']
        product_category = []
        for product in product_list:
            product_category.append(product['category'])
        if registration_flow == 'register':
            return Counter(self.default_products_category_list_domain_register) == Counter(product_category)
        elif registration_flow == 'existing':
            return Counter(self.default_products_category_list_domain_transfer) == Counter(product_category)
