from bs4 import BeautifulSoup
import re, time, allure


class hosting_regrade:
    upgrade_api_path = '/cgi/hosting/'
    host_id_path = '/cgi/hosting/#/'
    unable_to_add_to_cart = 'You are unable to upgrade to the same type of hosting'
    add_to_cart_success = 'Cart Checkout - '

    stuck_task_validation_prefix = 'The domain '
    stuck_task_validation_suffix = ' has pending payment processes. Try again in 5 or 10 minutes.'

    def __init__(self, testsetupObj):
        self.testsetup = testsetupObj

    @allure.step("Addition of a regraded Hosting Plan to the cart.")
    def add_plan_to_cart(self, Hosting_Regrade_DC):
        data = Hosting_Regrade_DC.req_data.dict(exclude_none=True)
        cookies = {
            'port2083': 'no',
            'test': '1',
            'country': 'IND',
            'Currency': 'INR',
            'Currency_Symbol': '%26%238377%3B',
            'currency': 'INR',
            'usession': self.testsetup.getCookies()['usession'],
            'admin_user': self.testsetup.getCookies()['admin_user'],
            'user_login': Hosting_Regrade_DC.domain_name,
        }
        headers = self.testsetup.getHeaders()
        Hosting_Regrade_DC.req_data.host_id = self.get_host_id(Hosting_Regrade_DC)
        data['host_id'] = Hosting_Regrade_DC.req_data.host_id

        isAddedToCart = False
        counter = 1
        count_limit = 1
        # Waiting for predefined time, for account to get provisioned with all invoice tasks completed.
        while (not isAddedToCart) and (counter <= count_limit):
            time.sleep(5)
            try:
                response = self.testsetup.mytarget.post(self.upgrade_api_path + Hosting_Regrade_DC.regrading_action,
                                                        headers=headers, cookies=cookies,
                                                        data=data, verify=self.testsetup.test_setup_dict['verify_ssl'])

                if response.assert_2xx():
                    try:
                        response.assert_in_body(self.add_to_cart_success + Hosting_Regrade_DC.domain_name)
                        print('succesfully added to cart within',5*counter,'(sec)')
                        isAddedToCart = True # Not really needed as we are returning value, so that will break the loop
                        return Hosting_Regrade_DC
                    except Exception as e:
                        if self.stuck_task_validation_prefix + Hosting_Regrade_DC.domain_name + self.stuck_task_validation_suffix in response.text:
                            print("Unable to add hosting product to cart.Payment task still in progress. Attempt #" + str(counter), 'Time Elasped (sec):', 5*counter)
                            if counter == count_limit:
                                raise Exception('Payment/Invoice related tasks still in progress. Unable to finish even after', 5*counter, '(sec)')
                            counter += 1
                        else:
                            raise Exception ("Un-expected error while adding hosting plan to cart. Response :" + str(response.text))
            except Exception as error:
                raise Exception ("Failed to add hosting plan to cart, assertion error : " + str(error) + str(response.text))

    # *************************************************************************************************
    #               Helper Methods
    # *************************************************************************************************
    @allure.step("Retrieve the host_id token.")
    def get_host_id(self, Hosting_Regrade_DC):
        cookies = {
            'test': '1',
            'port2083': 'no',
            'country': 'IND',
            'Currency': 'INR',
            'Currency_Symbol': '%26%238377%3B',
            'currency': 'INR',
            'usession': self.testsetup.getCookies()['usession'],
            'admin_user': self.testsetup.getCookies()['admin_user'],
        }

        headers = self.testsetup.getHeaders()
        params = (
            ('lil', '1'),
        )

        get_call_path = self.host_id_path + Hosting_Regrade_DC.regrading_action + '/' + \
                        Hosting_Regrade_DC.domain_name + '/cpanel'
        response = self.testsetup.mytarget.get(get_call_path, headers=headers, params=params, cookies=cookies)

        try:
            if response.assert_2xx():
                html = response.text
                return self.parse_host_id(html)
        except Exception as err:
            raise Exception("Failed to fetch host id with err :" + str(err) +
                            '\nFull Response\n' + str(response.text))

    def parse_host_id(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.findAll('script'):
            if "var page_settings = {" in str(tag):
                if "host_id" in str(tag):
                    m = re.search(r',"host_id":"([0-9]*?)",', tag.string)
                    if m:
                        host_id = int(m.group(1))
                        if isinstance(host_id, int):
                            return str(host_id)
                        else:
                            raise Exception(
                                "Unable to get host_id or host_id is not of type integer.\n host_id found is" +
                                m.group(1) + '\n Complete html reponse is :' + (html))
                    raise Exception('Failed to find host_id \n Complete html reponse is :' + str(html))
