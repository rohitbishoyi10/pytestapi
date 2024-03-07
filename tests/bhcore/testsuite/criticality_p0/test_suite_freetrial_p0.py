# **********   module imports  **************
from tests.bhcore.templates.free_trail.free_trial import *
from tests.bhcore.bhlib.dataclasses.template_flows.Free_Trial import *


# **********   Test Case  **************
@allure.testcase('https://jira.endurance.com/browse/BIQ-296', 'JIRA Link - BIQ 296')
@allure.testcase(
    'https://docs.google.com/spreadsheets/d/1SStrL4iIr2mYAOnDX1XJVntLmePiUiHs3D_Ol3oe9Wk/edit#gid=673187872',
    'Template Board Link')
@allure.suite('Signup Flow - Free Trial')
@allure.title('Free Trial Signup')
def test_free_trial_parmeterized_flow(hosting_plans, domain_action, payment_method, tlds, package_extras,free_trail_before_test):
    print(hosting_plans[0], hosting_plans[1], " | ", domain_action, " | ", tlds, " | ",package_extras, " | ",  payment_method)

    admin_user_token, testsetupObj = free_trail_before_test
    testsetupObj.test_setup_dict['populatefor'] = 'regular'
    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]
    testsetupObj.test_setup_dict['Package_Extras'] = package_extras

    free_trial_obj = Free_Trial()
    free_trial_obj.type = hosting_plans[0]
    free_trial_obj.subtype = hosting_plans[1]
    free_trial_obj.domain_type = domain_action
    free_trial_obj.payment_type = payment_method

    free_trial(testsetupObj).free_trail_signup_template(free_trial_obj)


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
    if "package_extras" in metafunc.fixturenames:
        metafunc.parametrize("package_extras", package_extras_info)


# *************   All Test Data (static) below this point  ************
hosting_plans_data = [('freetrial', 'blog')]
hosting_term_data = [1]
tlds_data = ['com']
payment_method_data = ['check']
domain_action_data = ['register', 'transfer','domainless']
# package_extras_info = [['domain_privacy_protection']]  #for 'register' domain_action only
package_extras_info = [[]]
