import allure
from tests.bhcore.bhlib.decorators.payment.check_decorator import Payment_Decorator
from tests.bhcore.bhlib.webcluster.assertion.freetrials.create_account import create_account
from tests.bhcore.bhlib.webcluster.assertion.freetrials.payment_receipt import payment_receipt
from tests.bhcore.bhlib.webcluster.cgi.setup_domain import setup_domain
from tests.bhcore.bhlib.mycluster.login import login
from tests.bhcore.bhlib.payment.payment import *
from tests.bhcore.bhlib.mycluster.cgi.account.forgot import forgot
from tests.bhcore.bhlib.mycluster.cgi.account_center.products import *
# data classes
from tests.bhcore.bhlib.dataclasses.hosting.Hosting import *
from tests.bhcore.bhlib.dataclasses.payment.Payment import *
from tests.bhcore.bhlib.dataclasses.mycluster.Account import *
from tests.bhcore.bhlib.dataclasses.mycluster.Login import *
#decorator
from tests.bhcore.bhlib.decorators.hosting.hosting_decorator import Hosting_Decorator

class free_trial:
    freetrial_flow_dict = {}

    def __init__(self, testsetup):
        self.testSetupObj = testsetup
        self.freetrial_flow_dict = copy.deepcopy(testsetup.test_setup_dict)

    def free_trail_signup_template(self, Free_Trial):
        hosting_data_dict = {}
        hosting_dc_obj = self.__select_hosting(Free_Trial, self.testSetupObj, hosting_data_dict)

        # validate Create Account page
        self.__validate_create_account_page(hosting_dc_obj.response_html, hosting_dc_obj)

        # Complete Payment
        paymentdc_obj = self.populate_Paymentdc(Free_Trial, hosting_dc_obj)
        paymentdc_obj = self.__purchase_hosting(self.testSetupObj, paymentdc_obj)

        # validate payment receipt
        self.__validate_payment_receipt(paymentdc_obj.payment_response)

        # Update Account Password
        updateAccPwd_Obj = self.__updateAccountPassword(self.populate_UpdateAccPwddc(paymentdc_obj))

        # Login to Account
        self.__loginToAccount()

        # Validate Account Purchased - as a Product
        self.__verify_product_info()


    @Hosting_Decorator
    @allure.step('Select Hosting Plan - FreeTrial Flow')
    def __select_hosting(self, Free_Trial, testSetupObj, hosting_data_dict):
        setupdomainObj = setup_domain(testSetupObj, Free_Trial)
        return setupdomainObj.select_hosting_plan(hosting_data_dict)

    @allure.step('Validation of the Created Account Pages in FreeTrial Flow')
    def __validate_create_account_page(self, html, Hostingdc_Obj):
        print("\n***********\n validate create account page\n**********\n")
        create_account_obj = create_account(html)
        create_account_obj.validate_disclaimer()
        create_account_obj.validate_pay_msg()
        create_account_obj.validate_pay_option()
        create_account_obj.validate_free_trial_title()
        create_account_obj.validate_free_trial_plan_package()
        if Hostingdc_Obj.req_data.domain_action == 'register':
            create_account_obj.validate_domain_registration()
            create_account_obj.validate_extra_package()
        print("\n***********\n create account page successfully validated\n**********\n")

    @allure.step('Set Account Password for Hosting Plan - FreeTrial Flow')
    def __updateAccountPassword(self, updateAccPwd_Obj):
        print("\n***************************\nUpdating Account Password...\n***************************\n")
        updateAccPwd_Obj = forgot(self.testSetupObj).update_account_forgot_password(
            updateAccPwd_Obj)  # The parameter passed
        # should be replaced once flow is complete with data_dict instead of setup dict.
        print("\n***************************\nAccoutn Password updated.\n***************************\n")
        return updateAccPwd_Obj

    @Payment_Decorator
    @allure.step('Purchase of a Hosting Plan in FreeTrial Flow')
    def __purchase_hosting(self, testSetupObj, Paymentdc_obj):
        pay = payment(testSetupObj)
        Paymentdc_obj = pay.pay(Paymentdc_obj)
        return Paymentdc_obj

    @allure.step('Validation of the Payment Receipt in FreeTrial Flow')
    def __validate_payment_receipt(self, html):
        print("\n***********\n validate payment receipt page\n**********\n")
        payment_receipt_obj = payment_receipt(self.testSetupObj, html)
        payment_receipt_obj.validate_receipt_description()
        payment_receipt_obj.validate_receipt_disclaimer()
        print("\n***********\n payment receipt page successfully validated\n**********\n")

    def populate_Paymentdc(self, Free_Trial, Hostingdc_Obj):
        paymentdc = Payment_DC()
        paymentdc.payment_type = Free_Trial.payment_type
        plan = self.testSetupObj.test_data[Free_Trial.type][Free_Trial.subtype]['plan']
        term = self.testSetupObj.test_data[Free_Trial.type][Free_Trial.subtype]['TERM']
        check_payload = Check_Payload_DC()
        check_payload.cust_id = Hostingdc_Obj.cust_id
        check_payload.data = Hostingdc_Obj.data_val
        check_payload.domain = Hostingdc_Obj.domain_name
        check_payload.domain_action = Hostingdc_Obj.req_data.domain_action
        check_payload.ir = Hostingdc_Obj.req_data.ir
        check_payload.sku = Hostingdc_Obj.req_data.sku
        check_payload.term = plan.replace('_plan=', ':') + '-' + term
        check_payload.paymethod = Free_Trial.payment_type
        check_payload.tos_agree = 'yes'
        check_payload.tax_id = Free_Trial.tax_id
        paymentdc.req_data = check_payload

        return paymentdc

    def populate_UpdateAccPwddc(self, Paymentdc):
        Update_Account_Password_DC.domain_name = Paymentdc.domain_name
        Update_Account_Password_DC.payment_token = Paymentdc.payment_token
        Update_Account_Password_DC.cust_id = Paymentdc.cust_id
        return Update_Account_Password_DC

    def __loginToAccount(self):
        print("\n***************************\nLogin to MyCluster...\n***************************\n")
        loginobj = login(self.testSetupObj)
        my_cluster_login_dc_obj = My_Cluster_Login_DC(bh_account = loginobj.bh_account, bh_password = loginobj.bh_password, usession = '', my_admin_token = '')
        my_cluster_login = loginobj.login_to_my_cluster(my_cluster_login_dc_obj)
        print("\n***************************\nSuccessfully Login to MyCluster...\n***************************\n")

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