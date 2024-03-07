import allure
from tests.bhcore.bhlib.dataclasses.mycluster.Login import My_Cluster_Login_DC
from tests.bhcore.bhlib.utils import html_util as util_handle
from tests.bhcore.bhlib.utils.testsetup import *
from tests.bhcore.bhlib.mycluster.cgi.account_center.products import *

# from tests.bhcore.variables import common
#
# ad_user = common.BH_AD_USERNAME_VARIABLE
# ad_pwd = common.BH_AD_PASSWORD_VARIABLE

class login():
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    path_cplogin = '/cgi-bin/cplogin'
    path_webhosting = '/web-hosting/signup'
    verifySSL = True

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, testsetup, isMyCluster=True, isVPN=True):
        self.testsetup = testsetup
        self.bh_account = testsetup.test_setup_dict['suite.random_domain_name']
        self.bh_password = testsetup.bh_pswd
        self.roster_user = testsetup.bh_ad_user
        self.roster_password = testsetup.bh_ad_pswd
        self.isMyCluster = isMyCluster
        self.isVPN = isVPN
        self.verifySSL = testsetup.test_setup_dict['verify_ssl']
        print('initiated...')

    # ********************************************************************************************
    #                               Robot Exposed KEYWORDS
    # ********************************************************************************************

    # def fetch_auth_token(self, dict, isMyCluster=True, isVPN=True):
    def fetch_auth_token(self, My_cluster_login, isMyCluster=True, isVPN=True):
        print('***** - CREDS...')
        if isMyCluster:
            resp_text, usession = self.login_to_my_cluster(self.bh_account,
                                                           self.bh_password)
            #self.testsetup.test_setup_dict['usession'] = usession
            My_cluster_login.usession = usession

            if isVPN:
                my_admin_token = self.Mycluser_cpanel_login(resp_text, usession)
                #self.testsetup.test_setup_dict['my_admin_token'] = my_admin_token
                My_cluster_login.my_admin_token = my_admin_token
        elif isVPN:
            my_admin_token = self.login_to_vpn()
            #self.testsetup.test_setup_dict['my_admin_token'] = my_admin_token
            My_cluster_login.my_admin_token = my_admin_token
        return My_cluster_login

    # ********************************************************************************************
    #                               Helper Methods
    # ********************************************************************************************
    def login_to_vpn(self):
        html = self.webhosting_signup()
        admin_token = self.cpanel_login(html)
        return admin_token

    @allure.step("Signup for a particular Web Hosting Plan in mycluster.")
    def webhosting_signup(self):
        print("*** webhosting_signup ***")
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()

        params = (
            ('cpanel_plan', 'wc_starter'),
        )
        response = self.testsetup.target.get(self.path_webhosting, headers=headers, params=params,
                                   cookies=cookies, verify=self.verifySSL)
        try:
            if response.assert_2xx():
                return response.text
        except Exception as error:
            raise Exception("Unable to do web hosting sign in, reason:" + str(error))

    @allure.step("cPanel login to retrieve admin_user token field in mycluster.")
    def cpanel_login(self, html):
        print('***cpanel_login***')
        cookies = self.testsetup.getCookies()
        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        headers = self.testsetup.getHeaders()

        data = {
            'redirect': util_handle.html_get_attr_value(html, 'redirect'),
            'cea_time': util_handle.html_get_attr_value(html, 'cea_time'),
            'cea_expires_min': util_handle.html_get_attr_value(html, 'cea_expires_min'),
            'admin_user': self.roster_user,
            'admin_pass': self.roster_password,
            'adminlogintok': util_handle.html_get_attr_value(html, 'adminlogintok')
        }

        response = self.testsetup.target.post(self.path_webhosting, headers=headers, cookies=cookies,
                                    data=data, verify=self.verifySSL)

        try:
            if response.assert_2xx() or response.assert_3xx():
                print(response.cp_cookies.get('admin_user'))
                return response.cp_cookies.get('admin_user')
        except Exception as error:
            raise Exception("Unable to do cpanel login, reason:" + str(error))

    @allure.step("myCluster Login.")
    def login_to_my_cluster(self, my_cluster_login):
        html = self.pre_login_to_my_cluster(None)
        print('***login_to_my_cluster***')
        cookies = self.testsetup.getCookies()
        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded', 'DNT': '1'})
        headers = self.testsetup.getHeaders()

        data = {
            # l_redirect => if it throws index out of bound/size exception, that means user is already logged in
            # and script is trying to relogin within same session. Debug script for that.
            'l_redirect': util_handle.html_get_attr_value(html, 'l_redirect'),
            'l_server_time': util_handle.html_get_attr_value(html, 'l_server_time'),
            'l_expires_min': util_handle.html_get_attr_value(html, 'l_expires_min'),
            'ldomain': my_cluster_login.bh_account,
            'lpass': my_cluster_login.bh_password,
        }

        response = self.testsetup.mytarget.post(self.path_cplogin, headers=headers, cookies=cookies, data=data, verify=self.verifySSL)

        try:
            if response.assert_2xx():
                usession = response.cp_cookies['usession']
                print("User session : "+ str(usession))
                self.testsetup.setCookies({'usession': usession})
                return response.text, usession
        except Exception as error:
            raise Exception("Unable to login to my cluster, reason:" + str(error))

    @allure.step("Pre Login to myCluster.")
    def pre_login_to_my_cluster(self, cookies=None):
        print("******pre_login_to_my_cluster********")
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        response = self.testsetup.mytarget.get(self.path_cplogin, headers=headers, cookies=cookies, verify=self.verifySSL)
        try:
            if response.assert_2xx():
                return response.text
        except Exception as error:
            raise Exception("Unable to complete pre login to my cluster, reason:" + str(error))

    @allure.step("myCluster cPanel login to retrieve admin_user token field.")
    def Mycluser_cpanel_login(self, html, usession):
        self.testsetup.setCookies({'test': '1', 'usession': usession})
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()

        data = {
            'redirect': util_handle.html_get_attr_value(html, 'redirect'),
            'cea_time': util_handle.html_get_attr_value(html, 'cea_time'),
            'cea_expires_min': util_handle.html_get_attr_value(html, 'cea_expires_min'),
            'admin_user': self.roster_user,
            'admin_pass': self.roster_password,
            'adminlogintok': util_handle.html_get_attr_value(html, 'adminlogintok')
        }
        response = self.testsetup.mytarget.post(self.path_cplogin, headers=headers, cookies=cookies, data=data,
                                      verify=self.verifySSL)
        try:
            if response.assert_2xx() or response.assert_3xx():
                return response.cp_cookies.get('admin_user')
        except Exception as error:
            raise Exception("Unable to perform cpanel login, reason:" + str(error))




# testSetupObj = testsetup('in', 'staging', ad_user, ad_pwd, bh_user='test-inapi-161009715060300400000497.com', bh_pswd='Test123!@#')
# testsetup.test_setup_dict['suite.random_domain_name'] = 'test-inapi-161009715060300400000497.com'
# loginobj = login(testSetupObj)
# my_cluster_login_dc_obj = My_cluster_login_dc(bh_account=loginobj.bh_account, bh_password=loginobj.bh_password, usession = '', my_admin_token = '')
# my_cluster_login = loginobj.login_to_my_cluster(my_cluster_login_dc_obj)
# prds = products(testSetupObj)
# prds.verify_products_info()