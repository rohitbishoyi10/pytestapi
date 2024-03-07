import allure
from tests.bhcore.bhlib.dataclasses.mycluster.Account import Update_Account_Password_DC
from tests.bhcore.bhlib.dataclasses.mycluster.Login import *
from tests.bhcore.bhlib.dataclasses.payment.Payment import Payment_DC, Check_Payload_DC
from tests.bhcore.bhlib.decorators.hosting.hosting_decorator import Hosting_Decorator
from tests.bhcore.bhlib.decorators.payment.check_decorator import Payment_Decorator
from tests.bhcore.bhlib.webcluster.cgi.setup_domain import setup_domain
from tests.bhcore.bhlib.mycluster.login import login
from tests.bhcore.bhlib.payment.payment import *
from tests.bhcore.bhlib.mycluster.cgi.account.forgot import forgot
from tests.bhcore.bhlib.mycluster.cgi.account_center.products import *

class signup_flow:
    signup_flow_dict = {}

    def __init__(self, testsetup):
        self.testSetupObj = testsetup
        self.signup_flow_dict = copy.deepcopy(testsetup.test_setup_dict)

    def signup_template(self, Signup_Flow):
        # Create an account
        hosting_dc_obj = self.__select_hosting(Signup_Flow, self.testSetupObj, {})

        # Complete Payment
        paymentdc_obj = self.populate_Paymentdc(Signup_Flow, hosting_dc_obj)
        paymentdc_obj = self.__purchase_hosting(self.testSetupObj, paymentdc_obj)

        if Signup_Flow.price_flag:
            return


        # # Update Account Password
        self.__updateAccountPassword(self.populate_UpdateAccPwddc(paymentdc_obj))

        # Login to Account
        self.__loginToAccount()

        # Validate Account Purchased - as a Product
        # if Signup_Flow.type == 'shared':
        #     self.__verify_product_info()

        return hosting_dc_obj.domain_name

    def signup_template_invalid_gst(self, Signup_Flow):
        # Create an account
        hosting_dc_obj = self.__select_hosting(Signup_Flow, self.testSetupObj, {})

        # Complete Payment
        paymentdc_obj = self.populate_Paymentdc(Signup_Flow, hosting_dc_obj)
        paymentdc_obj = self.__purchase_hosting(self.testSetupObj, paymentdc_obj)

        if paymentdc_obj.req_data.tax_id.startswith('27A'):
            if paymentdc_obj.payment_token == '':
                assert True

    @Hosting_Decorator
    @allure.step('Select Hosting Plan - Signup Flow')
    def __select_hosting(self, Signup_Flow, testSetupObj, hosting_data_dict):
        setupdomainObj = setup_domain(testSetupObj, Signup_Flow)
        return setupdomainObj.select_hosting_plan(hosting_data_dict)

    @allure.step('Set Account Password for Hosting Plan - Signup Flow')
    def __updateAccountPassword(self, updateAccPwd_Obj):
        print("***************************\nUpdating Account Password...\n***************************\n\n\n\n")
        updateAccPwd_Obj = forgot(self.testSetupObj).update_account_forgot_password(
            updateAccPwd_Obj)  # The parameter passed
        # should be replaced once flow is complete with data_dict instead of setup dict.
        print("\n\n\n\n\n***************************\nAccoutn Password updated.\n***************************")
        return updateAccPwd_Obj

    @Payment_Decorator
    @allure.step('Purchase of a Hosting Plan in Signup Flow')
    def __purchase_hosting(self, testSetupObj, Paymentdc_obj):
        pay = payment(testSetupObj)
        Paymentdc_obj = pay.pay(Paymentdc_obj)
        return Paymentdc_obj

    @allure.step('Login to the Hosting Plan purchased in Signup Flow')
    def __loginToAccount(self):
        loginobj = login(self.testSetupObj)
        my_cluster_login_dc_obj = My_Cluster_Login_DC(bh_account=loginobj.bh_account, bh_password=loginobj.bh_password,
                                                      usession='', my_admin_token='')
        my_cluster_login_response, usession = loginobj.login_to_my_cluster(my_cluster_login_dc_obj)

    @allure.step('Verify products available in Hosting plan purchased in Signup Flow')
    def __verify_product_info(self):
        product_to_search = self.create_product_info_dict()
        prds = products(self.testSetupObj)
        if prds.verify_products_info(product_to_search):
            assert True

    def create_product_info_dict(self):
        plan = self.testSetupObj.plans.split('=')[1]
        hosting_product = {
            'sku': self.testSetupObj.sku,
            'display_units_quantity': 1,
            'subtype': plan,
            'domain': self.testSetupObj.test_setup_dict['suite.random_domain_name'],
            # 'description': plan.capitalize() +' Web Hosting'
        }
        return [hosting_product]

    def populate_Paymentdc(self, Signup_Flow, Hostingdc_Obj):
        paymentdc = Payment_DC()
        paymentdc.payment_type = Signup_Flow.payment_type
        plan = self.testSetupObj.test_data[Signup_Flow.type][Signup_Flow.subtype]['plan']
        # term = self.testSetupObj.test_data['TERM']
        term = Signup_Flow.term
        paymentdc.plan = plan
        paymentdc.term = term
        paymentdc.Hosting_Type = Signup_Flow.type
        paymentdc.Subtype = Signup_Flow.subtype
        check_payload = Check_Payload_DC()
        check_payload.cust_id = Hostingdc_Obj.cust_id
        check_payload.data = Hostingdc_Obj.data_val
        check_payload.domain = Hostingdc_Obj.domain_name
        check_payload.domain_action = Hostingdc_Obj.req_data.domain_action
        check_payload.ir = Hostingdc_Obj.req_data.ir
        if Hostingdc_Obj.req_data.flow is not None:
            check_payload.flow = Hostingdc_Obj.req_data.flow
        check_payload.sku = Hostingdc_Obj.req_data.sku
        check_payload.term = plan.replace('_plan=', ':') + '-' + term
        check_payload.paymethod = Signup_Flow.payment_type
        check_payload.tos_agree = 'yes'
        check_payload.tax_id = Signup_Flow.tax_id
        paymentdc.req_data = check_payload
        return paymentdc

    def populate_UpdateAccPwddc(self, Paymentdc):
        UpdateAccPwddc = Update_Account_Password_DC()
        UpdateAccPwddc.domain_name = Paymentdc.domain_name
        UpdateAccPwddc.payment_token = Paymentdc.payment_token
        UpdateAccPwddc.cust_id = Paymentdc.cust_id
        return UpdateAccPwddc


