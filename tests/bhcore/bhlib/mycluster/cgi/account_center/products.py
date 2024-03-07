# from tests.bhcore.bhlib.utils.testsetup import testsetup
import json, warnings, allure

class products:
    path = '/cgi/account_center/api/products'
    verifySSL = True

    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.bh_acc_password = self.testsetup.bh_pswd
        self.verifySSL = testsetup.test_setup_dict['verify_ssl']

    def verify_products_info(self, products_to_lookup):
        print("Products available for look-up : \n"+str(str(products_to_lookup).encode('utf8')))
        products_in_user_account = self.get_current_products_list()
        self.product_lookup(products_in_user_account, products_to_lookup)

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    cookies = {
        'country' : 'IN'
    }

    @allure.step("Retrieve a list of all the available products.")
    def get_current_products_list(self):
        headers = self.testsetup.setHeaders(self.headers, ['Content-Type'])
        cookies = self.testsetup.setCookies(self.cookies)
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        print("Headers :"+str(headers))
        print("Cookies :" + str(cookies))
        response = self.testsetup.mytarget.get(self.path, headers=headers, cookies=cookies, verify=self.verifySSL)

        if response.assert_2xx():
            response_json = json.loads(response.text)
            if response_json['success'] == 1:
                return response_json['status']['current_products']
            else:
                assert response_json['error'] == "", 'Products API Response Contains error. Error msg retrieved :'+ \
                                                     response_json['error']+'\n Complete Response\n'+str(response.text)
                return response_json['status']['current_products']

    @staticmethod
    def product_lookup(current_products, expected_products_dict):
        print("\n\n**********\n All available Products \n*************\n" + str(str(current_products).encode('utf8')))
        if expected_products_dict is None:
            warnings.warn('Empty expected product list.')
            return True
        products_to_be_looked = len(expected_products_dict)
        counter = 0
        # For every product in the search list...
        for product_to_match in expected_products_dict:
            # Get the size of items to validate for every product...
            product_details_counter = len(product_to_match)
            # Inside all the products available in the user profile...
            for available_products in current_products:
                # Check the sku value for the lookup product to match in products available in user_profile...
                if product_to_match['sku'] == available_products['sku']:
                    counter += 1
                    # Match all the items from expected product dict & available products dict...
                    for key, value in product_to_match.items():
                        if product_details_counter == 0:
                            raise Warning('Products details to be looked for is already null.')
                        if key in available_products.keys():
                            # If the value expected matches with actual value...
                            if available_products[key] == value:
                                product_details_counter -= 1
                        # If all product details match, decrement count of pending product validations...
                        if product_details_counter == 0:
                            products_to_be_looked -= 1
                            break
            if products_to_be_looked + counter != len(expected_products_dict):
                raise AssertionError('Failed to validate product details.\n**********************'
                                     '\nFaulty Product\n' + str(str(product_to_match).encode('utf8'))+
                                     '\n**********************\nAll product list\n'+str(str(current_products).encode('utf8')))

        if products_to_be_looked == 0:
            print('All expected products are present in the user account.')
            return True
        else:
            print('All expected products are not present in the user account.')
            return False


# expected_pro_list = [
#     # {
#     #     'display_units_quantity': 1,
#     #     'sku': '68deb436',
#     #     'subtype': '',
#     #     'domain': 'test-productsapistaging.com',
#     #     'description': 'Domain Privacy + Protection'
#     # },
#     {
#         'display_units_quantity': 1,
#         'sku': 'c85378f7',
#         'subtype': 'basic',
#         'domain': 'test-inapi-161224060862474100103.com',
#         'description': 'Basic Web Hosting'
#     }
# ]
#
# testsetupObj = testsetup('in', 'staging', 'svcbluehostapac', 'Vf_z63&w=Zu=R+(U', bh_user='', bh_pswd='Test123!@#')
# products_obj = products(testsetupObj)
# user_products = products_obj.get_current_products_list()
# products_obj.product_lookup(user_products, expected_pro_list)
