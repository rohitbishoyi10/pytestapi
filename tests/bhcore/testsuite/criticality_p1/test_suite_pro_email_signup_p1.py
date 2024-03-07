"""
SDET            : Aditya Kumar
BOARD           : BIQ
JIRA Link       : https://jira.endurance.com/browse/BIQ-269
SYNERGY STORY   : NA
RTM Link        : NA
Evidence Link   : NA
Test Description : To test Professional Email - Hosting Signup/Purchase.
"""

# **********   Module Imports  **************
import allure, pytest
from tests.bhcore.templates.singnup_flow.signup_flow import signup_flow
from tests.bhcore.bhlib.dataclasses.template_flows.Signup_Flow import Signup_Flow as Pro_Email_Signup_Flow

# **********   Test Case  **************
@allure.testcase('https://jira.endurance.com/browse/BIQ-269', 'JIRA Link - BIQ 269')
@allure.testcase('https://docs.google.com/spreadsheets/d/1SStrL4iIr2mYAOnDX1XJVntLmePiUiHs3D_Ol3oe9Wk/edit#gid'
                 '=1183102642', 'Template Board')
@allure.suite('Signup Flow - Professional Email')
@allure.title('Professional Email - Signup')
def test_professional_email_signupFlow(hosting_plans, domain_action, payment_method, tlds, before_test):
    print(hosting_plans[0], hosting_plans[1], " | ", domain_action, " | ", tlds, " | ", payment_method)

    admin_user_token, testsetupObj = before_test
    testsetupObj.test_setup_dict['populatefor'] = 'professional_email'

    Pro_Email_Signup_Flow_obj = Pro_Email_Signup_Flow()
    Pro_Email_Signup_Flow_obj.type, Pro_Email_Signup_Flow_obj.subtype = hosting_plans[0], hosting_plans[1]
    Pro_Email_Signup_Flow_obj.domain_type = domain_action
    Pro_Email_Signup_Flow_obj.payment_type = payment_method
    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]

    signup_flow(testsetupObj).signup_template(Pro_Email_Signup_Flow_obj)


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

# All Hosting Type and Sub Type combos
business_plus = [('businessplus', 'basic'), ('businessplus', 'plus'), ('businessplus', 'choice_plus'), ('businessplus', 'pro')]
business_pro = [('businesspro', 'basic'), ('businesspro', 'plus'), ('businesspro', 'choice_plus'), ('businesspro', 'pro')]

hosting_plans_data = [*business_plus, *business_pro]
tlds_data = ['com']
payment_method_data = ['check']
# 'transfer' - as domain action =>  belongs to negative testing - but can't be tested as of now as this also works
domain_action_data = ['register', 'domainless']


# ================================================================================
#               EXPOSED METHODS TO BE USED BY OTHER DEPENDENT CLASSES
# ================================================================================


def replica_professional_email_signupFlow(hosting_plans, domain_action, payment_method, tlds, before_test_child):
    print("********\nHosting Type & Plan : ", hosting_plans[0], " | ", hosting_plans[1], "\tdomain action : ",
          domain_action, "\tPayment method : ", payment_method, " | ", tlds, "\n***********************")

    admin_user_token, testsetupObj = before_test_child
    testsetupObj.test_setup_dict['populatefor'] = 'professional_email'

    Pro_Email_Signup_Flow_obj = Pro_Email_Signup_Flow()
    Pro_Email_Signup_Flow_obj.type, Pro_Email_Signup_Flow_obj.subtype = hosting_plans[0], hosting_plans[1]
    Pro_Email_Signup_Flow_obj.domain_type = domain_action
    Pro_Email_Signup_Flow_obj.payment_type = payment_method
    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]

    domain_created = signup_flow(testsetupObj).signup_template(Pro_Email_Signup_Flow_obj)
    return domain_created
