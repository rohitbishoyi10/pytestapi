from tests.bhcore.bhlib.utils.html_util import *
import allure

class cart_details:
    path = '/hosting/cart'
    verifySSL = True
    page_Title = '<title>Cart Checkout - '

    def __init__(self, testsetup):
        self.testsetup = testsetup

    @allure.step("Retrieve the cart details in the Cart Checkout Page.")
    def get_cart_details(self, Hosting_Regrade_DC):

        cookies = {
            'port2083': 'no',
            'test': '1',
            'usession': self.testsetup.getCookies()['usession'],
            'admin_user': self.testsetup.getCookies()['admin_user'],
            'user_login': Hosting_Regrade_DC.domain_name,
        }
        headers = self.testsetup.getHeaders()

        response = self.testsetup.mytarget.get(self.path, headers=headers, cookies=cookies, verify=self.verifySSL)

        try:
            if response.assert_2xx():
                response.assert_in_body(self.page_Title + Hosting_Regrade_DC.domain_name + '</title>')
                html = response.text
                # Move below code to decorator
                regrade_data = read_products_table(html)
                charge_data = {
                    'subtotal': html_get_attr_value(html, 'subtotal'),
                    'locale_subtotal': html_get_attr_value(html, 'locale_subtotal'),
                    'usd_subtotal': html_get_attr_value(html, 'usd_subtotal'),
                    'total': html_get_attr_value(html, 'total'),
                    'locale_total': html_get_attr_value(html, 'locale_total'),
                    'usd_total': html_get_attr_value(html, 'usd_total'),
                    'cart_cust_id': html_get_attr_value(html, 'cart_cust_id'),
                    'cart_md5': html_get_attr_value(html, 'cart_md5'),
                    'purchase': html_get_attr_value(html, 'purchase'),
                    'ldomain': html_get_attr_value(html, 'ldomain'),
                    'new_cc_id': html_get_attr_value(html, 'new_cc_id'),
                    'card_secret': html_get_attr_value(html, 'card_secret'),
                    'cvv2_secret': html_get_attr_value(html, 'cvv2_secret'),
                    'host_id': Hosting_Regrade_DC.req_data.host_id
                }

                return regrade_data, charge_data
        except Exception as error:
            raise Exception("Failed to load Cart checkout page : " + str(error) + "\nFull Response\n", str(response.text))
