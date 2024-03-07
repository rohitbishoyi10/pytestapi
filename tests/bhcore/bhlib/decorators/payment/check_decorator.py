from tests.bhcore.bhlib.dataclasses.payment.Payment import Payment_DC, Tax_EST_DC, Tax_User_Info, Taxable_Products
from tests.bhcore.bhlib.payment.tax_est import Tax_Estimate
import json

from tests.bhcore.bhlib.utils.html_util import html_find_href, find_token, get_domain_custid_from_response, \
    check_for_text


class Payment_Decorator():
    in_gst_msg1 = 'THIS IS NOT A TAX INVOICE'
    in_gst_msg2 = 'As per latest government directives, eligible B2B invoices are required to be registered with the GSTN portal to be ' \
                  'considered as a valid Tax Invoice. We are currently processing registration of this invoice and you will receive your final Tax ' \
                  'Invoice by email shortly.'

    acceptable_resp_text = 'Your purchase was a success!'
    acceptable_invoice_text = 'Thank you for your purchase!'
    in_gst_invalid_msg = 'GSTIN is not valid for the selected state'

    def __init__(self, step_function):
        self.function = step_function

    def __call__(self, testsetup_obj, payment_dc):
        print('Inside Payment Decorator...')
        payment_dc = self.update_for_different_plans(payment_dc)
        payment_req_obj = payment_dc.req_data

        if testsetup_obj.test_setup_dict['local'] == 'in':
            payment_req_obj, tax_data_req = self.req_setup_for_in(payment_req_obj, testsetup_obj)
        elif testsetup_obj.test_setup_dict['local'] == 'sg':
            payment_req_obj, tax_data_req = self.req_setup_for_sg(payment_req_obj, testsetup_obj)
        elif testsetup_obj.test_setup_dict['local'] == 'com':
            self.req_setup_for_com(payment_dc)

        # .com Flow : UnboundLocalError: local variable 'tax_data_req' referenced before assignment
        tax_data_json = self.add_tax_json(testsetup_obj, tax_data_req)
        tax_data_dict = json.loads(tax_data_json)

        payment_req_obj.tax_json = tax_data_json
        payment_req_obj.tax_estimate = tax_data_dict['tax']

        payment_token, cust_id_cpanel, payment_response = self.function(self, testsetup_obj, payment_req_obj)
        if payment_req_obj.tax_id is not '':
            payment_token, cust_id_cpanel = self.validate_gst_flow(testsetup_obj, payment_response,
                                                                   payment_req_obj.tax_id)
        if 'price' in testsetup_obj.test_setup_dict.keys():
        # if 'price' in testsetup_obj.test_setup_dict:
            testsetup_obj.test_setup_dict['price_val']=self.verify_hosting_plan_price_IN(payment_response,testsetup_obj)
        payment_dc.payment_token = payment_token
        payment_dc.cust_id_cpanel = cust_id_cpanel
        payment_dc.payment_response = payment_response


        return payment_dc

    def validate_gst_flow(self, testsetup_obj, resp_text, gst_id):
        if testsetup_obj.test_setup_dict['local'] == 'in':
            if gst_id.startswith('27A'):
                if self.acceptable_resp_text in resp_text:
                    self.verify_gst_messages(resp_text)
                    text = resp_text
                    href = html_find_href(text, "auth?token=")
                    cust_id_cpanel = str(get_domain_custid_from_response(text))
                    payment_token = find_token(href)
                    print("Payment token " + str(payment_token))
                    return payment_token, cust_id_cpanel
            else:
                if self.in_gst_invalid_msg in resp_text:
                    return '', ''
                else:
                    raise Exception(
                        "Expected 'GSTIN is not valid for the selected state' NOT FOUND, reason:" + str(resp_text))

    def verify_gst_messages(self, resp_text):
        if self.in_gst_msg1 not in resp_text:
            raise Exception("Unable to find text for with GST purchases", "Actual : \n" + str(resp_text) + '\n', 'Expected : \n' + str(self.in_gst_msg1))
        if self.in_gst_msg2 not in resp_text:
            raise Exception("Unable to find text for with GST purchases", "Actual : \n" + str(resp_text) + '\n', 'Expected : \n' + str(self.in_gst_msg2))
        print('GST Message Successfully Verified.')

    def add_tax_json(self, testsetup_obj, tax_data_req):
        tax_est = Tax_Estimate(testsetup_obj)
        tax_json = tax_est.get_tax_json(tax_data_req)
        return tax_json

    def req_setup_for_in(self, payment_dc, testsetup_obj):
        payment_dc.brand = 'bluehost_in_dev_devees'
        payment_dc.tax_type = 'india_gst'
        payment_dc.currency = 'INR'
        payment_dc.country = 'IN'

        tax_data = Tax_EST_DC()
        tax_user_info = Tax_User_Info()
        tax_user_info.country = 'IN'
        tax_user_info.city = 'Mumbai'
        tax_user_info.zip = '400063'
        tax_user_info.address = 'NESCO IT Park, Western Express Highway'
        tax_user_info.state = 'MH'
        tax_user_info.cust_id = payment_dc.cust_id
        tax_user_info.lastname = 'Barua'
        tax_user_info.currency = 'INR'

        taxable_prods_arr = []
        if testsetup_obj.test_setup_dict['Hosting_Type'] == 'freetrial' and payment_dc.domain_action == 'register':
            taxable_prods = Taxable_Products()
            taxable_prods.sku = testsetup_obj.test_data['freetrial']['packageInfo']['primary_domain_registration']['sku']
            taxable_prods.term = testsetup_obj.test_data['freetrial']['packageInfo']['primary_domain_registration']['term']
            taxable_prods_arr.append(taxable_prods)

        if 'Package_Extras' in testsetup_obj.test_setup_dict.keys():
            for addons in testsetup_obj.test_setup_dict['Package_Extras']:
                print("addons")
                if not addons == 'domain_privacy_protection':
                    addOns, plan = addons.split("#")
                    taxable_prods = Taxable_Products()
                    taxable_prods.sku = testsetup_obj.test_data['Package_Extras'][addOns][plan]['sku']
                    if addOns == "codeguard":
                        taxable_prods.term = testsetup_obj.test_data['TERM']
                    else:
                        taxable_prods.term = testsetup_obj.test_data['Package_Extras'][addOns][plan]['term']
                    taxable_prods_arr.append(taxable_prods)
                else:
                    taxable_prods = Taxable_Products()
                    taxable_prods.sku = testsetup_obj.test_data['Package_Extras'][addons]['sku']
                    taxable_prods.term = testsetup_obj.test_data['Package_Extras'][addons]['term']
                    taxable_prods_arr.append(taxable_prods)

        taxable_prods = Taxable_Products()
        taxable_prods.sku = payment_dc.sku
        taxable_prods.term = payment_dc.term.split('-')[1]
        taxable_prods_arr.append(taxable_prods)

        tax_data.user_info = tax_user_info
        tax_data.products = taxable_prods_arr

        if 'Package_Extras' in testsetup_obj.test_setup_dict.keys():
            for addons in testsetup_obj.test_setup_dict['Package_Extras']:
                if 'domain_privacy_protection' == addons:
                          payment_dc.privacy = 'on'
                elif 'codeguard#basic' == addons:
                          payment_dc.codeguard_basic = 'on'
                elif 'marketgoo#start' == addons:
                          payment_dc.marketgoo_start = 'on'
                elif 'sitelock#essential' == addons:
                          payment_dc.sitelock_essential = 'on'
                elif 'office365#business_essentials' == addons:
                          payment_dc.office365_business_essentials = 'on'

        return payment_dc, tax_data

    def req_setup_for_com(self, payment_dc):
        payment_dc.brand = ''
        self.check_pmt_dc.tax_type = 'india_gst'
        self.check_pmt_dc.currency = 'INR'
        self.check_pmt_dc.country = 'IN'

    def req_setup_for_sg(self, payment_dc, testsetup_obj):
        # Check Data
        payment_dc.brand = 'bluehostasia'
        payment_dc.country = 'SG'
        payment_dc.address = '71+Robinson+Rd'
        payment_dc.city = 'Singapore'
        payment_dc.zip = '068895'
        payment_dc.phone_cc = '65'
        payment_dc.phone = '66816768'
        payment_dc.tax_type = 'sg'
        payment_dc.currency = 'SGD'

        # Tax call data
        tax_data = Tax_EST_DC()
        tax_user_info = Tax_User_Info()
        tax_user_info.country = 'SG'
        tax_user_info.city = 'Singapore'
        tax_user_info.zip = '068895'
        tax_user_info.address = '71 Robinson Rd'
        tax_user_info.state = ''
        tax_user_info.cust_id = payment_dc.cust_id
        tax_user_info.lastname = 'Kumar'
        tax_user_info.currency = 'SGD'

        taxable_prods_arr = []
        if 'Package_Extras' in testsetup_obj.test_setup_dict.keys():
            for addOns in testsetup_obj.test_setup_dict['Package_Extras']:
                taxable_prods = Taxable_Products()
                taxable_prods.sku = testsetup_obj.test_data['Package_Extras'][addOns]['sku']
                if addOns == "codeguard_basic":
                    taxable_prods.term = testsetup_obj.test_data['TERM']
                else:
                    taxable_prods.term = testsetup_obj.test_data['Package_Extras'][addOns]['term']
                taxable_prods_arr.append(taxable_prods)

        taxable_prods = Taxable_Products()
        taxable_prods.sku = payment_dc.sku
        taxable_prods.term = payment_dc.term.split('-')[1]
        taxable_prods_arr.append(taxable_prods)

        tax_data.user_info = tax_user_info
        tax_data.products = taxable_prods_arr

        return payment_dc, tax_data

    def update_for_different_plans(self, payment_data):
        data = payment_data.req_data
        plans = payment_data.plan
        term = payment_data.term
        if 'ecom' in payment_data.Hosting_Type.lower():
            data.flow = 'woocommerce'
            data.ir = 'house^HOMEPAGEBYPASS^https://www.beta.bluehost.in/web-hosting/signup?flow=woocommerce&' + plans
        elif 'dedicated' in payment_data.Hosting_Type.lower():
            print('Its Dedicated...')
            data.experience = 'legacy'
            data.stockcpanel = 'legacy'
            data.term = 'dedicated:' + payment_data.Subtype + '-' + term
        if data.domain_action == 'domainless':
            print('Payment being done for Domainless flow...')
            # data['domain_action'] = 'domainless'
            data.privacy = None
        elif data.domain_action == 'transfer':
            print('Payment being done for Existing flow...')
            # data['domain_action'] = 'transfer'
            data.privacy = None
        return payment_data

    def verify_hosting_plan_price_IN(self, payment_response,testsetupObj):
        try:

            if testsetupObj.test_setup_dict['local'] == 'in':
                test = 'Total: ' + '₹' + testsetupObj.test_setup_dict['price']
            else:
                test = 'Total: ' + '$' + testsetupObj.test_setup_dict['price']
            self.price = check_for_text(payment_response, test)

            assert self.price == test
            print("Price validation done" + str(self.price))
            return True

        except Exception as error:
            raise Exception("Price validation fails" + str(payment_response))


