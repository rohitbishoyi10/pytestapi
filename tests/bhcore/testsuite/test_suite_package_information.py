"""
SDET            : Manish Patwal
BOARD           : BIQ
JIRA Link       : https://jira.endurance.com/browse/BIQ-256
Test Description : To test package information details for different terms.
"""

from tests.bhcore.templates.singnup_flow.signup_flow import signup_flow
from tests.bhcore.bhlib.dataclasses.template_flows.Signup_Flow import Signup_Flow as Package_Information
import pytest

@pytest.mark.indiaReady
# @pytest.mark.skip(reason="Debugging tests. Skipping this")
def test_package_information_terms_flow(hosting_plans, domain_action, payment_method, tlds, before_test):
    print(hosting_plans[0], hosting_plans[1], " | ", domain_action, " | ", tlds, " | ", payment_method)

    admin_user_token, testsetupObj = before_test
    testsetupObj.test_setup_dict['populatefor'] = 'regular'
    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]

    pack_inform_obj = Package_Information()
    pack_inform_obj.type = hosting_plans[0]
    pack_inform_obj.subtype = hosting_plans[1]
    pack_inform_obj.term = hosting_plans[2]
    pack_inform_obj.domain_type = domain_action
    pack_inform_obj.payment_type = payment_method
    pack_inform_obj.price_flag=True



    signup_flow(testsetupObj).signup_template(pack_inform_obj)


def pytest_generate_tests(metafunc):
    if "hosting_plans" in metafunc.fixturenames:
        metafunc.parametrize("hosting_plans", hosting_plans_data)
    if "domain_action" in metafunc.fixturenames:
        metafunc.parametrize("domain_action", domain_action_data)
    if "payment_method" in metafunc.fixturenames:
        metafunc.parametrize("payment_method", payment_method_data)
    if "tlds" in metafunc.fixturenames:
        metafunc.parametrize("tlds", tlds_data)



# *************   All Test Data (static) below this point  ************

# All Hosting Type and Sub Type combos
shared_hosting_plans = [('shared', 'basic', '12'),('shared', 'basic', '24')]
ecom_hosting_plans = [('ecom', 'starter', '12'),('ecom', 'starter', '24')]
wppro_hosting_plans = [('wppro', 'build', '3'),('wppro', 'build', '6'),('wppro', 'build', '12'),('wppro', 'build', '24')]

hosting_plans_data = [*shared_hosting_plans,*wppro_hosting_plans, *ecom_hosting_plans]
tlds_data = ['com']
payment_method_data = ['check']
domain_action_data = ['register' ,'domainless','transfer']


