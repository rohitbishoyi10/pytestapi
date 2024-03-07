# from tests.bhcore.bhlib.utils.testsetup import testsetup
# import os, sys
import time, allure, warnings
from tests.bhcore.bhlib.utils.html_util import *


class admin():
    path = '/admin/user/cpanel/{domain_name}'
    affiliates_id: str = None
    affiliates_Tracking:str = None
    affiliates_Referer:str = None


    def __init__(self, testsetup):
        self.testsetup = testsetup

    @allure.step('Validate Affiliates Accounts ID in I_Cluster')
    def validate_affilates_acounts_id_in_Icluster(self, hosting_data_dict):
        domain_name = hosting_data_dict.domain_name
        self.path = self.path.replace('{domain_name}', domain_name)
        self.affiliates_id, self.affiliates_Tracking, self.affiliates_Referer = hosting_data_dict.req_data.ir.split('^')
        headers = self.testsetup.getHeaders()
        admin_user = self.testsetup.getCookies()['admin_user']
        cookies = {
            'admin_user': admin_user,
        }

        response = self.testsetup.itarget.get(self.path, headers=headers, params=domain_name, cookies=cookies)

        try:
            if response.assert_2xx():
                data_dict = read_aff_account_tracking_from_icluster(response.text)
                if not (data_dict['aff_account'] == self.affiliates_id and data_dict[
                    'aff_tracking'] == self.affiliates_Tracking and data_dict['aff_referer'] == self.affiliates_Referer):
                    print('Expected Data :', self.affiliates_id, self.affiliates_Tracking, self.affiliates_Referer)
                    print('Actual Data :', data_dict['aff_account'], data_dict['aff_tracking'],
                          data_dict['aff_referer'])
                    raise Exception("Affiliates expected data doesn't matches with Actual Data." + str(response.text))
                else:
                    print('Succesfully validated Affiliates details in cpanel.')
                    return data_dict
        except Exception as error:
            raise Exception("Validation failed at cpanel response."+str(error) + str(response.text))
