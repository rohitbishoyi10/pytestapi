import allure
from tests.bhcore.bhlib.utils import html_util as handle


class signup():
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    path = '/web-hosting/signup'

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.admin_user = testsetup.bh_ad_user
        self.admin_password = testsetup.bh_ad_pswd
        self.local = testsetup.local
        self.env = testsetup.env
        self.verifySSL = testsetup.verify_ssl

    # ********************************************************************************************
    #                               Robot Exposed KEYWORDS
    # ********************************************************************************************
    def get_admin_user_token(self):
        html = self.webhosting_signup()
        admin_token = self.cpanel_login(html, self.admin_user, self.admin_password)
        print('ADMIN TOKEN: ' + str(admin_token))
        return admin_token

    # ********************************************************************************************
    #                               Helper Methods
    # ********************************************************************************************
    @allure.step("Signup for a particular Web Hosting Plan in webcluster.")
    def webhosting_signup(self,  login_dect = None):
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        params = (
            ('cpanel_plan', 'basic'),
        )
        if self.testsetup.free_trial:
            params = (
                ('cpanel_plan', 'blog'),
            )
        response = self.testsetup.target.get(self.path, headers=headers, params=params, cookies=cookies, verify= self.verifySSL)
        return response.content

    @allure.step("cPanel login to retrieve admin_user token field in webcluster.")
    def cpanel_login(self, html, admin_user, admin_password):
        cookies = self.testsetup.getCookies()
        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        headers = self.testsetup.getHeaders()
        data = {
            'redirect': handle.html_get_attr_value(html, 'redirect'),
            'cea_time': handle.html_get_attr_value(html, 'cea_time'),
            'cea_expires_min': handle.html_get_attr_value(html, 'cea_expires_min'),
            'admin_user': admin_user,
            'admin_pass': admin_password,
            'adminlogintok': handle.html_get_attr_value(html, 'adminlogintok')
        }
        response = self.testsetup.target.post(self.path, headers=headers, cookies=cookies, data=data, verify=self.verifySSL)
        if response.assert_2xx() or response.assert_3xx():
            admin_user_token = response.cp_cookies.get('admin_user')
        if admin_user_token is None:
            raise Exception("Unable to fetch admin user token for user:"+self.admin_user+"\nComplete API response - Method: cpanel_login:-\n"+str(response))
        print(admin_user_token)
        return admin_user_token
