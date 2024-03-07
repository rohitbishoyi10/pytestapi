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
from tests.bhcore.bhlib.icluster.cgi.db_cpanel import *
from tests.bhcore.bhlib.icluster.cgi.admin.admin import admin


class affiliates_signup_flow:
    signup_flow_dict = {}

    def __init__(self, testsetup):
        self.testSetupObj = testsetup
        self.signup_flow_dict = copy.deepcopy(testsetup.test_setup_dict)

    def affiliates_signup_template(self, Affiliates_Signup_Flow):
        # Create an account

        hosting_dc_obj = self.__select_hosting(Affiliates_Signup_Flow, self.testSetupObj, {})

        # Complete Payment
        # Paymentdc_obj = self.__purchase_hosting(self.populate_Paymentdc(Affiliates_Signup_Flow, hosting_dc_obj))
        paymentdc_obj = self.populate_Paymentdc(Affiliates_Signup_Flow, hosting_dc_obj)
        paymentdc_obj = self.__purchase_hosting(self.testSetupObj, paymentdc_obj)

        # # Update Account Password
        self.__updateAccountPassword(self.populate_UpdateAccPwddc(paymentdc_obj))

        # Login to Account
        self.__loginToAccount()

        # Add Product Validation Here :
        # ToDo

        # # Affiliates validation via db_query :
        # Disbaling this due to time bound dependency.. instead alternative is being used below.
        # self.affiliates_db_query_validation(paymentdc_obj)

        # Add cPanel Layer Affiliates ID & Token assertion :
        self.__validate_affiliatesIDToken_At_cPanel(hosting_dc_obj)

    # Select Hosting Plan

    @Hosting_Decorator
    @allure.step('Select Affiliates redirected Hosting Plan')
    def __select_hosting(self, Affiliates_Signup_Flow, testSetupObj, hosting_data_dict):
        setupdomainObj = setup_domain(testSetupObj, Affiliates_Signup_Flow)
        return setupdomainObj.select_hosting_plan_via_affiliates(hosting_data_dict)

    # Purchase Selected Hosting Plan
    @Payment_Decorator
    @allure.step('Purchase Affiliates redirected Hosting plan')
    def __purchase_hosting(self, testSetupObj, Paymentdc_obj):
        pay = payment(testSetupObj)
        Paymentdc_obj = pay.pay(Paymentdc_obj)
        return Paymentdc_obj

    # Set Account Password for account purchased
    @allure.step('Set Account Password for Affiliates redirected Hosting plan')
    def __updateAccountPassword(self, updateAccPwd_Obj):
        print("***************************\nUpdating Account Password...\n***************************\n\n\n\n")
        updateAccPwd_Obj = forgot(self.testSetupObj).update_account_forgot_password(updateAccPwd_Obj)
        print("\n\n\n\n\n***************************\nAccoutn Password updated.\n***************************")
        return updateAccPwd_Obj

    # Login to the hosting account
    @allure.step('Login to Hosting plan purchased via affiliates')
    def __loginToAccount(self):
        loginobj = login(self.testSetupObj)
        my_cluster_login_dc_obj = My_Cluster_Login_DC(bh_account=loginobj.bh_account, bh_password=loginobj.bh_password,
                                                      usession='', my_admin_token='')
        my_cluster_login_response, usession = loginobj.login_to_my_cluster(my_cluster_login_dc_obj)

    @allure.step('Validate Affiliates led Hosting Account Purchased using db_query')
    def affiliates_db_query_validation(self, Paymentdc_obj):
        db_cpanel(self.testSetupObj).validate_affilates_order_relayerid(Paymentdc_obj.cust_id_cpanel)

    @allure.step('Verify products available in Hosting plan purchased via affiliates')
    def __verify_product_info(self):
        product_to_search = self.create_product_info_dict()
        prds = products(self.testSetupObj)
        if prds.verify_products_info(product_to_search):
            assert True

    @allure.step('Verify Affiliates - Account ID & token in the cpanel manager of the account.')
    def __validate_affiliatesIDToken_At_cPanel(self, Affiliates_Signup_Flow):
        admin(self.testSetupObj).validate_affilates_acounts_id_in_Icluster(Affiliates_Signup_Flow)


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

    def populate_Paymentdc(self, Affiliates_Signup_Flow, Hostingdc_Obj):
        paymentdc = Payment_DC()
        paymentdc.payment_type = Affiliates_Signup_Flow.payment_type
        plan = self.testSetupObj.test_data[Affiliates_Signup_Flow.type][Affiliates_Signup_Flow.subtype]['plan']
        term = self.testSetupObj.test_data['TERM']
        check_payload = Check_Payload_DC()
        check_payload.cust_id = Hostingdc_Obj.cust_id
        check_payload.data = Hostingdc_Obj.data_val
        check_payload.domain = Hostingdc_Obj.domain_name
        check_payload.domain_action = Hostingdc_Obj.req_data.domain_action
        check_payload.ir = Hostingdc_Obj.req_data.ir
        check_payload.sku = Hostingdc_Obj.req_data.sku
        check_payload.term = plan.replace('_plan=', ':') + '-' + term
        check_payload.paymethod = Affiliates_Signup_Flow.payment_type
        check_payload.tos_agree = 'yes'
        check_payload.tax_id = Affiliates_Signup_Flow.tax_id

        if Affiliates_Signup_Flow.affiliates:
            check_payload.no_cookie_brick = 'on'
            check_payload.ir = Affiliates_Signup_Flow.ir

        paymentdc.req_data = check_payload

        return paymentdc

    def populate_UpdateAccPwddc(self, Paymentdc):
        UpdateAccPwddc = Update_Account_Password_DC()
        UpdateAccPwddc.domain_name = Paymentdc.domain_name
        UpdateAccPwddc.payment_token = Paymentdc.payment_token
        UpdateAccPwddc.cust_id = Paymentdc.cust_id
        return UpdateAccPwddc

