from tests.bhcore.bhlib.dataclasses.mycluster.Hositng_Regrading import *
from tests.bhcore.bhlib.dataclasses.mycluster.Login import *
from tests.bhcore.bhlib.dataclasses.payment.Charge import Charge_Cart_Payload_DC, Charge_DC

from tests.bhcore.bhlib.mycluster.login import login
from tests.bhcore.bhlib.mycluster.cgi.hosting.hosting_regrade import hosting_regrade
from tests.bhcore.bhlib.payment.payment import *
from tests.bhcore.bhlib.mycluster.cgi.hosting.cart_details import *
from tests.bhcore.bhlib.payment.charge import *
from tests.bhcore.bhlib.mycluster.cgi.account_center.products import *


class account_regrade:
    account_regrade_dict = {}

    def __init__(self, testsetup):
        self.testSetupObj = testsetup
        self.account_regrade_dict = copy.deepcopy(testsetup.test_setup_dict)

    def account_regrading_template(self, Upgrade_Downgrade_Flow):
        self.testSetupObj.test_setup_dict['suite.random_domain_name'] = Upgrade_Downgrade_Flow.domain_name

        # ================================================================================
        # Account Upgrade-Downgrade Flow
        # ================================================================================

        # Login to Account
        self.__loginToAccount()

        # Add target plan to cart
        hosting_regrade_dc = self.populate_Hosting_RegradeDC(Upgrade_Downgrade_Flow)
        hosting_regrade_dc = self.__select_plan_to_regrade(hosting_regrade_dc)

        # Get Card Details
        regrade_data, cart_data_dc = self.__get_cart_details(hosting_regrade_dc)


        # Make Payment for plan Up/Down Re-grade
        self.__charge_cart_items(regrade_data, cart_data_dc, Upgrade_Downgrade_Flow)

        # Validate for plan upgrade/downgrade
        self.__verify_product_info(Upgrade_Downgrade_Flow)


    # ================================================================================
    # Template Step Definitions
    # ================================================================================

    # Login to the hosting account
    def __loginToAccount(self):
        loginobj = login(self.testSetupObj)
        my_cluster_login_dc_obj = My_Cluster_Login_DC(bh_account=loginobj.bh_account, bh_password=loginobj.bh_password,
                                                      usession='', my_admin_token='')
        loginobj.login_to_my_cluster(my_cluster_login_dc_obj)

    #Adding hosting plan to cart
    def __select_plan_to_regrade(self, Hosting_Regrade_DC):
       return hosting_regrade(self.testSetupObj).add_plan_to_cart(Hosting_Regrade_DC)

    #Retrieve the items added to the cart
    def __get_cart_details(self, hosting_regrade_dc):
        return cart_details(self.testSetupObj).get_cart_details(hosting_regrade_dc)

    #Purchase the items present in the cart
    def __charge_cart_items(self, regrade_data, cart_data_dc, Upgrade_Downgrade_Flow):
        Charge_DC_Obj = self.populate_Chargedc(regrade_data, cart_data_dc, Upgrade_Downgrade_Flow)
        return charge(self.testSetupObj).charge_for_cart_items(Charge_DC_Obj)

    #Validate for plan updation in user's account
    def __verify_product_info(self, Upgrade_Downgrade_Flow):
        product_to_search = self.create_product_info_dict(Upgrade_Downgrade_Flow)
        prds = products(self.testSetupObj)
        if prds.verify_products_info(product_to_search):
            assert True

    # ================================================================================
    # Template Step Definitions - Helper Methods Below
    # ================================================================================

    def populate_Hosting_RegradeDC(self, Upgrade_Downgrade_Flow):
        hosting_regrade_dc = Hosting_Plan_Regrading_DC()
        hosting_regrade_dc.regrading_action = Upgrade_Downgrade_Flow.regrading_action
        hosting_regrade_dc.domain_name = Upgrade_Downgrade_Flow.domain_name
        hosting_regrade_dc.type = Upgrade_Downgrade_Flow.type
        hosting_regrade_dc.subtype_active = Upgrade_Downgrade_Flow.subtype_active
        hosting_regrade_dc.subtype_switch = Upgrade_Downgrade_Flow.subtype_switch
        hosting_regrade_dc.payment_type = Upgrade_Downgrade_Flow.payment_type

        payload_data = Hosting_Regrade_Payload_DC()
        payload_data.url_hash = '#/' + hosting_regrade_dc.regrading_action + '/' + hosting_regrade_dc.domain_name + '/cpanel'
        payload_data.product = 'cpanel:' + hosting_regrade_dc.subtype_switch
        payload_data.term = self.testSetupObj.test_data['TERM']
        hosting_regrade_dc.req_data = payload_data

        return hosting_regrade_dc

    def populate_Chargedc(self, regrade_data, cart_data_dc, Upgrade_Downgrade_Flow):
        charge_dc = Charge_DC()

        charge_dc.host_id = cart_data_dc['host_id']
        charge_dc.domain_name = Upgrade_Downgrade_Flow.domain_name
        charge_dc.payment_type = Upgrade_Downgrade_Flow.payment_type

        charge_payload = Charge_Cart_Payload_DC()
        charge_payload.subtotal = cart_data_dc['subtotal']
        charge_payload.locale_subtotal = cart_data_dc['locale_subtotal']
        charge_payload.usd_subtotal = cart_data_dc['usd_subtotal']
        charge_payload.total = cart_data_dc['total']
        charge_payload.locale_total = cart_data_dc['locale_total']
        charge_payload.usd_total = cart_data_dc['usd_total']
        charge_payload.cart_cust_id = cart_data_dc['cart_cust_id']
        charge_payload.cart_md5 = cart_data_dc['cart_md5']
        charge_payload.purchase = cart_data_dc['purchase']
        charge_payload.ldomain = cart_data_dc['ldomain']
        charge_payload.new_cc_id = cart_data_dc['new_cc_id']
        charge_payload.card_secret = cart_data_dc['card_secret']
        charge_payload.cvv2_secret = cart_data_dc['cvv2_secret']
        charge_payload.plan_data = regrade_data
        charge_dc.req_data = charge_payload

        return charge_dc


    def create_product_info_dict(self, Upgrade_Downgrade_Flow):
        self.testSetupObj.populate_hosting_test_data(Upgrade_Downgrade_Flow.type, Upgrade_Downgrade_Flow.subtype_switch)
        plan = self.testSetupObj.plans.split('=')[1]
        hosting_product = {
            'sku': self.testSetupObj.sku,
            'display_units_quantity': 1,
            'subtype': plan,
            'domain': self.testSetupObj.test_setup_dict['suite.random_domain_name'],
            # 'description': plan.capitalize() +' Web Hosting'
        }
        return [hosting_product]