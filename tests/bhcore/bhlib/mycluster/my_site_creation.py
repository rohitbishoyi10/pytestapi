from tests.bhcore.bhlib.mycluster.cgi.account_center.products import *

class Mysite_Creation:
    # ********************************************************************************************
    #                               Class Variables
    # ********************************************************************************************
    user_id_path = '/api/users'
    HOSTING = 'hosting'
    WORDPRESS = 'wordpress'
    acceptable_resp_text = '"success":true'

    # ********************************************************************************************
    #                               Constructor
    # ********************************************************************************************
    def __init__(self, testsetupObj):
        self.testsetup = testsetupObj
        print('initiated...')

    def get_user_id(self):
        cookies = self.testsetup.getCookies()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://my.beta.bluehost.in/hosting/app',
            'Cache-Control': 'max-age=0',
        }

        response = self.testsetup.mytarget.get(self.user_id_path, headers=headers, cookies=cookies)
        try:
            if response.assert_2xx():
                # response.assert_in_body(self.testsetup.domain_name)
                html = response.text
                user_id = str(json.loads(html)["user_id"])
                return user_id
        except Exception as error:
            raise Exception("Failed to get User ID : " + str(error) + "\nFull Response\n",
                            str(response.text))

    def mysite_Creation(self, mysite_DC):
        domain_name = self.testsetup.test_setup_dict['suite.random_domain_name']
        mysite_path = self.user_id_path + "/" + self.get_user_id() + "/" + self.HOSTING + "/" + domain_name + "/" + self.WORDPRESS
        print("**********\nCreating mySite\n*************")
        cookies = {
            'port2083': 'no',
            'currency': 'INR',
            'country': 'IN',
            'usession': self.testsetup.getCookies()['usession'],
            'admin_user': self.testsetup.getCookies()['admin_user'],
            'user_login': domain_name,
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=utf-8',
            'Connection': 'keep-alive',
        }

        print('***********')
        print(headers)
        print(cookies)
        print('***********')
        data = mysite_DC.dict(exclude_none=True)

        print("MySite Data : \n" + str(data))
        try:
            response = self.testsetup.mytarget.post(mysite_path, headers=headers, cookies=cookies, timeout=60,
                                                    json=data)
            print('Response ', response.text)
            exp_str = self.acceptable_resp_text
            # Add a flow success, assertion here apart from basic 2xx.
            if response.assert_2xx():
                response.assert_in_body(exp_str)
                print(response.text)
                return response.text
            else:
                raise Exception(
                    'Unable to validate successfull creation of mysite. Check in response below :' + str(response.text))
        except Exception as error:
            raise Exception("Unable to create mySite, reason:" + str(error) + str(response.text))
