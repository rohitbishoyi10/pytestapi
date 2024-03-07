"""
SDET            : Aditya Kumar
JIRA Link       : https://jira.endurance.com/browse/BIQ-225, https://jira.endurance.com/browse/BIQ-259
SYNERGY STORY   : NA
RTM Link        : NA
Evidence Link   : NA
Test Description : To test purchase of Hosting Plan via an affiliates route and its validation.
"""

# **********   Module Imports  **************
import allure, pytest
from tests.bhcore.templates.singnup_flow.affiliates_signup_flow import affiliates_signup_flow
from tests.bhcore.bhlib.dataclasses.template_flows.Signup_Flow import Signup_Flow as Affiliates_DC

# **********   Test Case  **************
@allure.suite('Affiliates Scenarios')
@allure.title('Affiliates Sign Up Flow')
def test_hosting_parmeterized_flow(hosting_plans, domain_action, payment_method, tlds, before_test):
    print(hosting_plans[0], hosting_plans[1], " | ", domain_action, " | ", tlds, " | ", payment_method)

    admin_user_token, testsetupObj = before_test
    testsetupObj.test_setup_dict['populatefor'] = 'regular'

    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]

    Affiliates_Signup_flow = Affiliates_DC()
    Affiliates_Signup_flow.type = hosting_plans[0]
    Affiliates_Signup_flow.subtype = hosting_plans[1]
    Affiliates_Signup_flow.domain_type = domain_action
    Affiliates_Signup_flow.payment_type = payment_method
    Affiliates_Signup_flow.affiliates = True

    affiliates_signup_flow(testsetupObj).affiliates_signup_template(Affiliates_Signup_flow)


# **********   Test Data Generator  **************
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
hosting_plans_data = [('ecom', 'starter')]
tlds_data = ['com']
payment_method_data = ['check']
domain_action_data = ['register', 'transfer', 'domainless']
