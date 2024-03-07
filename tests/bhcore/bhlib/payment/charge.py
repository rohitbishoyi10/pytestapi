import allure

class charge:
    path = '/cgi/cart/charge'
    verifySSL = True
    success_msg = 'Thank you for your purchase! If you experience any problems related to this order, please contact us at'

    def __init__(self, testsetup):
        self.testsetup = testsetup

    @allure.step('Loading of the Cart Checkout Page with charged Items.')
    def charge_for_cart_items(self, Charge_DC):

        cookies = {
            'port2083': 'no',
            'test': '1',
            'usession': self.testsetup.getCookies()['usession'],
            'admin_user': self.testsetup.getCookies()['admin_user'],
            'user_login': Charge_DC.domain_name,
        }
        headers = self.testsetup.getHeaders()

        data = Charge_DC.req_data.dict(exclude_none=True)
        data.pop('plan_data')
        data.update(Charge_DC.req_data.plan_data)

        response = self.testsetup.mytarget.post(self.path, headers=headers, cookies=cookies, data=data, verify=self.verifySSL)

        try:
            if response.assert_2xx():
                response.assert_in_body(self.success_msg)
                html = response.text
                return html
        except Exception as error:
            raise Exception("Failed to load Cart checkout page : " + str(error) + "\nFull Response\n", str(response.text))
