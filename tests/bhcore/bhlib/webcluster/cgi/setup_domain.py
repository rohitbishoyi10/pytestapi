import json, allure
from tests.bhcore.bhlib.utils.html_util import *


class setup_domain:
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    path = '/web-hosting/signup'
    sku = {}
    plans = {}
    acceptable_response_text_prefix = 'The domain '
    acceptable_response_text_suffix = ' is available!'
    create_account_page_title = 'Create Your Account'
    verifySSL = True
    vpv = '/signup/billing/pick_site_success/'
    affiliates_success_prefix = '<h1>Warning:</h1> non-house affiliate "<span class="js_p_aff">'
    affiliates_success_suffix = '</span>" detected but NOT skipped because you have permission to pay by check!'
    non_house_affiliate_checkbox = '"keep-non-house-affiliate-checkbox" checked="checked"'

    # Commented below variable, are not needed but might be helpful in future. Should be removed if usage not found.
    # domain_action = Enum(new='register', existing='transfer', domainless ='domainless')

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, testsetup, signup_flow_dc):
        self.testsetup = testsetup
        self.verifySSL = testsetup.test_setup_dict['verify_ssl']
        # self.sku, self.plans = self.testsetup.populate_hosting_test_data(signup_flow_dc.type, signup_flow_dc.subtype)
        self.sku, self.plans = self.testsetup.populate_hosting_test_data(signup_flow_dc)
        self.signup_flow_dc = signup_flow_dc

    # ********************************************************************************************
    #                               Template Exposed Methods
    # ********************************************************************************************
    def select_hosting_plan(self, hosting_data_dict):
        # Select a Hosting Plan - Create a new domain
        if hosting_data_dict['domain_action'] == 'register':
            return self.select_hosting_plan_new_domain(hosting_data_dict)
        # Select a hosting plan - Domain less account
        elif hosting_data_dict['domain_action'] == "domainless":
            return self.select_domainless_hosting_plan(hosting_data_dict)
        # Select a Hosting Plan - Using existing domain
        elif hosting_data_dict['domain_action'] == 'transfer':
            return self.select_hosting_plan_with_existing_domain(hosting_data_dict)
        else:
            raise Exception("The flow selected is not recognized. Please select from \n(1) Register,\n(2) Transfer,"
                            "\n(3) Domainless.\nSelected Value is:" + hosting_data_dict['domain_action'])

    def select_hosting_plan_via_affiliates(self, hosting_data_dict):
        # Select a Hosting Plan - Create a new domain
        if hosting_data_dict['domain_action'] == 'register':
            return self.select_hosting_plan_new_domain_via_Affiliates(hosting_data_dict)
        # Select a hosting plan - Domain less account
        elif hosting_data_dict['domain_action'] == "domainless":
            return self.select_domainless_hosting_plan_via_Affiliates(hosting_data_dict)
        # Select a Hosting Plan - Using existing domain
        elif hosting_data_dict['domain_action'] == 'transfer':
            return self.select_hosting_plan_with_existing_domain_via_Affiliates(hosting_data_dict)
        else:
            raise Exception("The flow selected is not recognized. Please select from \n(1) Register,\n(2) Transfer,"
                            "\n(3) Domainless.\nSelected Value is:" + hosting_data_dict['domain_action'])



    # ********************************************************************************************
    #                               Select Hosting Plans - Usual Flow
    # ********************************************************************************************
    @allure.step("Select New Domain Hosting Plan.")
    def select_hosting_plan_new_domain(self, hosting_dc_dict):
        print('Selecting a Hosting Plan - Using a New Domain')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        domain_name = hosting_dc_dict['domain'] + "." + hosting_dc_dict['tld']
        print("\n", headers, "\n", cookies, "\n", str(hosting_dc_dict))
        resp = self.testsetup.target.post(self.path, data=hosting_dc_dict, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        text = None
        try:
            exp_str = self.acceptable_response_text_prefix + domain_name + self.acceptable_response_text_suffix
            if resp.assert_2xx() and resp.assert_in_body(exp_str):
                text = resp.text
                custid = html_get_attr_value(text, 'cust_id')
                data_val = html_get_attr_value(text, 'data')
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error))
        return text, custid, domain_name, data_val

    @allure.step("Select Domainless Hosting Plan.")
    def select_domainless_hosting_plan(self, hosting_dc):
        print('Selecting a Hosting Plan - Domain Less')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        resp = self.testsetup.target.post(self.path, data=hosting_dc, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        try:
            if resp.assert_2xx() and resp.assert_in_body(self.create_account_page_title):
                text = resp.text
                dataLayer = self.get_dataLayer(text)
                if self.data_check(dataLayer, self.vpv + 'domainless', 'domainless') == '':
                    custid = html_get_attr_value(text, 'cust_id')
                    data_val = html_get_attr_value(text, 'data')
                    allocatedDomain = html_get_attr_value(text, 'domain')
                    print('************************\nCustID: ' + str(
                        custid) + '\nDomainless Domain: ' + allocatedDomain + '\ndata: ' + str(
                        data_val) + '\n************************\n')
        except Exception as error:
            print('************************\nDEBUG : Response Text \n************************\n' + str(resp.text))
            raise Exception("Unable to Select Domain, reason:" + str(error))
        return text, custid, allocatedDomain, data_val

    @allure.step("Select Existing Domain Hosting Plan.")
    def select_hosting_plan_with_existing_domain(self, hosting_dc):
        print('Selecting a Hosting Plan - Existing Domain')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        resp = self.testsetup.target.post(self.path, data=hosting_dc, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        try:
            if resp.assert_2xx():
                text = resp.text
                dataLayer = self.get_dataLayer(text)
                if self.data_check(dataLayer, self.vpv + 'transfer', 'existing domain') == '':
                    custid = html_get_attr_value(text, 'cust_id')
                    data_val = html_get_attr_value(text, 'data')
                    allocatedDomain = html_get_attr_value(text, 'domain')
                    print('************************\nCustID: ' + str(
                        custid) + '\nExisting Domain: ' + allocatedDomain + '\ndata: ' + str(
                        data_val) + '\n************************\n')
        except Exception as error:
            print('************************\nDEBUG : Response Text \n******************************\n' +
                  str(resp))
            raise Exception("Unable to Select Domain, reason:" + str(error))
        return text, custid, allocatedDomain, data_val

    # ********************************************************************************************
    #                               Select Hosting Plans - Affiliates Flow
    # ********************************************************************************************
    @allure.step("Select Affiliates redirected New Domain Hosting Plan.")
    def select_hosting_plan_new_domain_via_Affiliates(self, hosting_dc_dict):
        print('Selecting a Hosting Plan - Using a New Domain')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        domain_name = hosting_dc_dict['domain'] + "." + hosting_dc_dict['tld']
        print("\n", headers, "\n", cookies, "\n", str(hosting_dc_dict))
        resp = self.testsetup.target.post(self.path, data=hosting_dc_dict, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        text = None
        try:
            exp_str = self.acceptable_response_text_prefix + domain_name + self.acceptable_response_text_suffix
            if resp.assert_2xx() and resp.assert_in_body(exp_str):
                text = resp.text
                # Validating first for proper affiliate by its id & then validate if the non-house affiliate checkbox is checked
                resp.assert_in_body(
                    self.affiliates_success_prefix + self.signup_flow_dc.affiliates_id + self.affiliates_success_suffix) and resp.assert_in_body(
                    self.non_house_affiliate_checkbox)
                custid = html_get_attr_value(text, 'cust_id')
                data_val = html_get_attr_value(text, 'data')
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error) + 'Full HTML Response :' + text)
        return text, custid, domain_name, data_val

    @allure.step("Select Affiliates redirected Domainless Hosting Plan.")
    def select_domainless_hosting_plan_via_Affiliates(self, hosting_dc):
        print('Selecting a Hosting Plan - Domain Less')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        resp = self.testsetup.target.post(self.path, data=hosting_dc, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        try:
            if resp.assert_2xx() and resp.assert_in_body(self.create_account_page_title):
                # Validating first for proper affiliate by its id & then validate if the non-house affiliate checkbox is checked
                resp.assert_in_body(
                    self.affiliates_success_prefix + self.signup_flow_dc.affiliates_id + self.affiliates_success_suffix) and resp.assert_in_body(
                    self.non_house_affiliate_checkbox)
                text = resp.text
                dataLayer = self.get_dataLayer(text)
                if self.data_check(dataLayer, self.vpv + 'domainless', 'domainless') == '':
                    custid = html_get_attr_value(text, 'cust_id')
                    data_val = html_get_attr_value(text, 'data')
                    allocatedDomain = html_get_attr_value(text, 'domain')
                    print('************************\nCustID: ' + str(
                        custid) + '\nDomainless Domain: ' + allocatedDomain + '\ndata: ' + str(
                        data_val) + '\n************************\n')
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error) + 'Full HTML Response :' + resp.text)
        return text, custid, allocatedDomain, data_val

    @allure.step("Select Affiliates redirected Existing Domain Hosting Plan.")
    def select_hosting_plan_with_existing_domain_via_Affiliates(self, hosting_dc):
        print('Selecting a Hosting Plan - Existing Domain')
        headers, cookies, custid, data_val = self.formulate_hosting_flow()
        resp = self.testsetup.target.post(self.path, data=hosting_dc, cookies=cookies, headers=headers,
                                          verify=self.verifySSL)
        try:
            if resp.assert_2xx():
                # Validating first for proper affiliate by its id & then validate if the non-house affiliate checkbox is checked
                resp.assert_in_body(
                    self.affiliates_success_prefix + self.signup_flow_dc.affiliates_id + self.affiliates_success_suffix) and resp.assert_in_body(
                    self.non_house_affiliate_checkbox)
                text = resp.text
                dataLayer = self.get_dataLayer(text)
                if self.data_check(dataLayer, self.vpv + 'transfer', 'existing domain') == '':
                    custid = html_get_attr_value(text, 'cust_id')
                    data_val = html_get_attr_value(text, 'data')
                    allocatedDomain = html_get_attr_value(text, 'domain')
                    print('************************\nCustID: ' + str(
                        custid) + '\nExisting Domain: ' + allocatedDomain + '\ndata: ' + str(
                        data_val) + '\n************************\n')
        except Exception as error:
            raise Exception("Unable to Select Domain, reason:" + str(error) + 'Full HTML Response :' + resp.text)
        return text, custid, allocatedDomain, data_val

    # ********************************************************************************************
    #                               Helper Methods
    # ********************************************************************************************

    def formulate_hosting_flow(self):
        headers = self.create_headers()
        cookies = self.testsetup.getCookies()
        custid = data_val = ''
        return headers, cookies, custid, data_val

    @staticmethod
    def get_dataLayer(html):
        data = {}
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.findAll('script'):
            if 'dataLayer' in str(tag):
                m = re.search(r"dataLayer = (.*?);", tag.string)
                if m:
                    for dic in json.loads(m.group(1)):
                        data.update(dic)
                    print(str(data))
                    return data
        return data

    @staticmethod
    def split_domain_name(domain_name):
        names = domain_name.split('.')
        return names[0], names[1]

    def create_headers(self):
        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        return self.testsetup.getHeaders()

    def create_cookies(self, admin_user_token):
        self.testsetup.setCookies({'admin_user': admin_user_token})
        return self.testsetup.getCookies()

    def populate_data(self, hosting_dc):
        print('creating hosting domain data...')
        ir_host = 'house^HOMEPAGEBYPASS^' + self.testsetup.get_host()
        data = hosting_dc.req_data
        data = data.dict(exclude_none=True)
        data['ir'] = ir_host + '/web-hosting/signup?' + self.plans
        data['sku'] = self.sku
        if 'ecom' in hosting_dc.Hosting_Type.lower():
            data['flow'] = 'woocommerce'
            data['ir'] = ir_host + '/web-hosting/signup?flow=woocommerce&' + self.plans
        if hosting_dc.domain_action == 'register':
            name, tld = self.split_domain_name(hosting_dc.domain_name)
            data['domain'] = name
            data['tld'] = tld
        if hosting_dc.domain_action == 'transfer':
            data['domain'] = hosting_dc.domain_name
        print('Domain Request Data :- \n' + str(data))
        return data

    def data_check(self, data_dict, sucessText, domainOption):
        if data_dict != {}:
            if data_dict['hosting_subtype'] == self.plans.split('=')[1] and sucessText in str(data_dict['vpv']):
                print('Hosting Sub type : ' + data_dict['hosting_subtype'] + '\n vpv : ' + data_dict['vpv'])
                return ''
            else:
                print('Expected Data : ' + data_dict['hosting_subtype'] + '\t' + sucessText)
                print('Actual Data : ' + self.plans.split('=')[1] + '\t' + data_dict['vpv'])
                raise Exception(
                    "Unable to setup " + domainOption + " hosting account. Check above comparision between Expected "
                                                        "and Actual values.")
        else:
            raise Exception("Unable to retrieve data layer." + str(data_dict))
