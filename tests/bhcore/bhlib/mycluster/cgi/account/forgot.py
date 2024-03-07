import time, allure
from tests.bhcore.bhlib.utils import html_util as util_handle



class forgot:
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    path = '/cgi/forgot/update'
    authPath = '/hosting/forgot/auth'
    acc_chk_path = '/cgi/forgot/account_setup_check'

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.bh_acc_password = self.testsetup.bh_pswd

    # ********************************************************************************************
    #                               Robot Exposed KEYWORDS
    # ********************************************************************************************
    @allure.step("Update the Password of an Existing Account.")
    def update_account_forgot_password(self, UpdateAccPwd_Obj):
        # self.bh_acc_password = critical_test_dict['suite.bh_acc_password']
        print('token_value=' + str(UpdateAccPwd_Obj.payment_token))
        html = self.chek_auth_token(UpdateAccPwd_Obj.cust_id, UpdateAccPwd_Obj.payment_token,
                                    UpdateAccPwd_Obj.domain_name)
        admins_user = self.testsetup.test_setup_dict['admin_token']
        # admins_user = self.do_auth(html, self.testsetup.bh_ad_user, self.testsetup.bh_ad_pswd,
        #                            UpdateAccPwd_Obj.domain_name, UpdateAccPwd_Obj.cust_id)
        # print('*******\nAdmin User:'+admins_user+'\n*******\n')
        if admins_user is None:
            raise Exception('Aborting the test as admin_user_token is None.')
        self.auth2(UpdateAccPwd_Obj.cust_id, admins_user, UpdateAccPwd_Obj.domain_name,
                   UpdateAccPwd_Obj.payment_token)
        data = {
            'pw1': self.bh_acc_password,
            'pw2': self.bh_acc_password,
            'token': UpdateAccPwd_Obj.payment_token,
            'tos': 'true'
        }
        err_check = '"has_errors":1'
        exp_error = 'Your account is in the process of being created, please wait a few minutes to set your password.'
        # response = self.execute_put_request(admins_user, 'https://my.beta.bluehost.in/cgi/forgot/update', data)
        # txt = response.text
        isAccountCreated = False
        counter = 1
        while (not isAccountCreated) and (counter < 20):
            time.sleep(10)
            try:
                txt = self.execute_put_request(admins_user, data)
            except ConnectionError as e:
                time.sleep(5)
                print('Got Connection Error Exception, so retrying')
                txt = self.execute_put_request(admins_user, data)
                print('Response Text::' + txt)
            if err_check in txt:
                if exp_error in txt:
                    counter += 1
                    print('response has errors:' + txt + '. Retrying after 5seconds...\nAttempt: #' + str(counter))
                else:
                    raise Exception('Unable to update the account password, error details available below :\n' + txt)
            else:
                isAccountCreated = True
                break
        if isAccountCreated:
            print('Account Password Successfully Updated after ' + str(counter) + ' attempts.')
        else:
            raise Exception('Unable to update the account password even after ' + str(counter) + ' attempts.')

        # print('Update Password Response :\n' + str(txt))
        # This is for debugging purpose, Will change once test stabilize
        self.account_setup_check(admins_user, UpdateAccPwd_Obj.payment_token,
                                 UpdateAccPwd_Obj.domain_name, UpdateAccPwd_Obj.cust_id)
        UpdateAccPwd_Obj.setPwd_response = txt
        # UpdateAccPwd_Obj.admin_user = admins_user
        return UpdateAccPwd_Obj

    # ********************************************************************************************
    #                               Helper Methods
    # ********************************************************************************************
    @allure.step("Verify Authorized Token.")
    def chek_auth_token(self, custid, token, domain_name):
        self.testsetup.setCookies({'port2083': 'no',
                                   'custid': custid,
                                   'user_login': domain_name, })
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        params = (
            ('token', token),
            ('origin', 'signup'),
        )
        response = self.testsetup.mytarget.get(self.authPath, headers=headers, params=params, cookies=cookies,
                                               verify=self.testsetup.test_setup_dict['verify_ssl'])
        try:
            if response.assert_2xx():
                return response.text
        except Exception as error:
            raise Exception("Method : chek_auth_token => Unable to verify auth token, reason:" + str(error)+
                            "\n Complete Response\n"+str(response.text))

    @allure.step("Do Authorization and Retrieve admin_user token field.")
    def do_auth(self, html_resp, admin_userId, admin_password, domain_name, custid):
        self.testsetup.setCookies({'port2083': 'no',
                                      'custid': custid,
                                      'user_login': domain_name}, ['admin_user'])

        cookies = self.testsetup.getCookies()

        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        headers = self.testsetup.getHeaders()

        data = {
            'redirect': util_handle.html_get_attr_value(html_resp, 'redirect'),
            'cea_time': util_handle.html_get_attr_value(html_resp, 'cea_time'),
            'cea_expires_min': util_handle.html_get_attr_value(html_resp, 'cea_expires_min'),
            'admin_user': admin_userId,
            'admin_pass': admin_password,
            'adminlogintok': util_handle.html_get_attr_value(html_resp, 'adminlogintok')
        }
        counter = 0
        admin_user_token = None
        while counter < 2 and admin_user_token is None:
            response = self.testsetup.mytarget.post(self.authPath, headers=headers, cookies=cookies, data=data,
                                                    verify=self.testsetup.test_setup_dict['verify_ssl'])
            try:
                if response.assert_2xx():
                    admin_user_token = response.cp_cookies.get('admin_user')
                    if admin_user_token is None and counter > 0:
                        print("Data :"+str(data)+"\n")
                        print("admin user token is NONE. Response HTML below :\n" + str(response.text))
                        raise Exception("Method : do_auth => Aborting the test as admin_user_token is None.")
                    elif counter == 0 and admin_user_token is None:
                        counter += 1
                        print("Retrying do_auth after 5sec. Failed to get admin_user_token.")
                        time.sleep(5)
            except Exception as error:
                raise Exception(
                    "Method : do_auth => Aborting the test as failed to get 2xx response., reason:" + str(error)+
                            "\n Complete Response\n"+str(response.text))

        print('Admin Token:: ' + str(admin_user_token))
        return admin_user_token

    @allure.step("First Authorization Call and retrieval of status_code token .")
    def auth1(self, html, custid, admin_user, domain_name):
        self.testsetup.setCookies({'port2083': 'no',
                                      'custid': custid,
                                      'admin_user': admin_user,
                                      'user_login': domain_name, })
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()

        params = (
            ('step', 'auth'),
            ('cea_time', util_handle.html_get_attr_value(html, 'cea_time')),
            ('redirect', util_handle.html_get_attr_value(html, 'redirect')),
            ('adminlogintok', util_handle.html_get_attr_value(html, 'adminlogintok')))

        response = self.testsetup.mytarget.get(self.authPath, headers=headers, params=params,
                                               cookies=cookies, verify=self.testsetup.test_setup_dict['verify_ssl'])
        print(response.status_code)

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://my.beta.bluehost.in/hosting/forgot/auth?step=auth&cea_time=1602101881&redirect=%2Fhosting%2Fforgot%2Fauth%3Fstep%3Dauth%26origin%3Dsignup%26token%3Daa3547e107e52c4cdf0051a6975fc9f5b1cfdbc89f7c314e855b12bc82f2f46fa3c828578d7c3772f65b6a1ab47519e72574403f9db61f2ad313535f92d883a8043f8946fe1e58e9f2b5f5c1708e22a172ceb30e5332864d8203ae44684e5682a1fb8fc95e645c03c124853fedab299233e403045056ed7f19a335a750f82ed09885355832537a89def8f6d326e084c6f11b7d2eb71c073e779e4cea895b98754f662666f83580efa847e4fd995e7f7f74e5b7b8346b0fda3d3651a86582e202026804d332821702cddb2b6b114ca93266d5dde0ca4020cd&adminlogintok=a_l_t%3A63824558895746', headers=headers, cookies=cookies)

    @allure.step("Second Authorization Call.")
    def auth2(self, custid, admin_user, domain_name, token):
        self.testsetup.setCookies({'port2083': 'no',
                                      'custid': custid,
                                      'user_login': domain_name,
                                      'admin_user': admin_user})
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        params = (
            ('step', 'auth'),
            ('origin', 'signup'),
            ('token', token),)
        response = self.testsetup.mytarget.get(self.authPath, headers=headers, params=params,
                                               cookies=cookies, verify=self.testsetup.test_setup_dict['verify_ssl'])
        try:
            if response.assert_2xx():
                print('Auth2 Call is successful')
        except Exception as error:
            raise Exception("Method : auth2 => Failed to obtain 2xx status code. reason:" + str(error)+
                            "\n Complete Response\n"+str(response.text))

    @allure.step("Checking of the account setup by selecting a domain.")
    def account_setup_check(self, admin_user, token, domain_name, custid):
        self.testsetup.setCookies({'port2083': 'no',
                                      'custid': custid,
                                      'user_login': domain_name,
                                      'admin_user': admin_user})
        cookies = self.testsetup.getCookies()
        headers = self.testsetup.getHeaders()
        params = (
            ('token', token),
            ('_', '1602102494316'),
        )
        response = self.testsetup.mytarget.get(self.acc_chk_path, headers=headers, params=params, cookies=cookies,
                                               verify=self.testsetup.test_setup_dict['verify_ssl'])
        try:
            response.assert_2xx()
        except Exception as error:
            raise Exception("Method : account_setup_check => Unable to Select Domain, reason:" + str(error)+
                            "\n Complete Response\n"+str(response.text))

    @allure.step("Retrieval of text token and execution of PUT request.")
    def execute_put_request(self, admin_user, data):
        headers = self.create_request_header()
        cookies = self.create_cookies(admin_user)
        response = self.testsetup.mytarget.put(self.path, headers=headers, cookies=cookies,
                                               data=data, verify=self.testsetup.test_setup_dict['verify_ssl'])
        try:
            if response.assert_2xx():
                return str(response.text)
        except Exception as error:
            raise Exception("Method : execute_put_request => Unable to Select Domain, reason:" + str(error)+
                            "\n Complete Response\n"+str(response.text))

    def create_request_header(self):
        self.testsetup.setHeaders({'Content-Type': 'application/x-www-form-urlencoded'})
        return self.testsetup.getHeaders()

    def create_cookies(self, admin_user):
        self.testsetup.setCookies({'admin_user': admin_user})
        return self.testsetup.getCookies()
