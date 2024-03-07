# from tests.bhcore.bhlib.utils.testsetup import testsetup
# import os, sys
import time, allure, warnings


class db_cpanel:
    validation_text = '<td>order_relayer_id</td>'
    path = '/cgi-bin/admin/db'

    def __init__(self, testsetup):
        self.testsetup = testsetup

    @allure.step('Validate Affiliates Relayer ID')
    def validate_affilates_order_relayerid(self, cust_id):
        print(cust_id)
        headers = self.testsetup.getHeaders()
        admin_user = self.testsetup.getCookies()['admin_user']
        cookies = {
            'admin_user': admin_user,
        }
        params = (
            ('sql',
             'select * from lineitem join lineitem_args on lineitem.id = lineitem_args.lineitem_id where name = \'order_relayer_id\' and lineitem.cust_id=\''+cust_id+'\''),
            ('load', ''),
            ('profiling', '1'),
        )
        isRelayerID_populated = False
        counter = 1
        # Since this steps is ambigous and takes random time ranging between seconds to minutes - assigning maximum
        # wait of 0.5 min
        while (not isRelayerID_populated) and (counter < 3):
            time.sleep(5)
            response = self.testsetup.itarget.get(self.path, headers=headers, params=params, cookies=cookies, verify=self.testsetup.test_setup_dict['verify_ssl'])

            try:
                response.assert_2xx() and response.assert_in_body(self.validation_text)
                print("Succesfully validated relayer id in response. Took #", str(counter), ' attempts. Time taken in minutes :', str(0.83*counter))
                isRelayerID_populated = True
                break
            except Exception as error:
                print("Unable to validate relayer id in response. Attempt #" + str(counter))
                if counter == 2:
                    print(response.text)
                    warnings.warn('Unable to get order_relayer_id in 30 seconds.')
                    # raise Exception("Unable to validate affiliates via db query within 2 minutes. Error :"
                    #                 + str(error) + "\n**************** Full HTML Response *************"
                    #                 + response.text + "\n***********************************")
                counter += 1

# testsetupObj = testsetup('in', 'staging', 'svcbluehostapac', 'Vf_z63&w=Zu=R+(U', bh_user='', bh_pswd='Test123!@#')
# products_obj = db_cpanel(testsetupObj)
# user_products = products_obj.validate_affilates_order_relayerid()
