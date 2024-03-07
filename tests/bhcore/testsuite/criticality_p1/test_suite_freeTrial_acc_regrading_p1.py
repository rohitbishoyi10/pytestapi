# **********   Module Imports  **************
import allure, pytest
from tests.bhcore.templates.Account_Regrading.account_regrading import account_regrade
from tests.bhcore.bhlib.dataclasses.template_flows.Account_Regrading_Flow import Account_Regrading_Flow


# **********   Test Case  **************
@allure.testcase('https://jira.endurance.com/browse/BIQ-296', 'JIRA Link - BIQ 296')
@allure.testcase(
    'https://docs.google.com/spreadsheets/d/1SStrL4iIr2mYAOnDX1XJVntLmePiUiHs3D_Ol3oe9Wk/edit#gid=1052942211',
    'Template Board Link')
@allure.suite('Upgrade/Downgrade Flow')
@allure.title('FreeTrial Account Upgrade Downgrade')
@pytest.mark.skip(reason="This is a test data dependent test case. It will be enabled later on")
def test_my_site_creation_parmeterized_flow(domain_name, regrading_information, payment_method, before_test):
    print(domain_name, " | ", regrading_information, " | ", payment_method)
    admin_user_token, testsetupObj = before_test

    Account_Regrading_Flow_obj = Account_Regrading_Flow()
    Account_Regrading_Flow_obj.regrading_action = regrading_information[3]
    Account_Regrading_Flow_obj.domain_name = domain_name
    Account_Regrading_Flow_obj.type, Account_Regrading_Flow_obj.subtype_active, Account_Regrading_Flow_obj.subtype_switch = \
    regrading_information[0], regrading_information[1], regrading_information[2]
    Account_Regrading_Flow_obj.payment_type = payment_method

    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['Hosting_Type'] = Account_Regrading_Flow_obj.type
    testsetupObj.test_setup_dict['Subtype'] = Account_Regrading_Flow_obj.subtype_switch

    account_regrade(testsetupObj).account_regrading_template(Account_Regrading_Flow_obj)


# **********   Test Data Generator  **************
def pytest_generate_tests(metafunc):
    if "domain_name" in metafunc.fixturenames:
        metafunc.parametrize("domain_name", domain_name_data)
    if "regrading_information" in metafunc.fixturenames:
        metafunc.parametrize("regrading_information", regrading_information_data)
    if "payment_method" in metafunc.fixturenames:
        metafunc.parametrize("payment_method", payment_method_data)


# # *************   All Test Data (static) below this point  ************
regrading_information_data = [
                     ('shared', 'blog', 'basic', 'upgrade'),
#                     ('shared', 'basic', 'plus', 'upgrade'), ('shared', 'basic', 'choice_plus', 'upgrade'), ('shared', 'basic', 'pro', 'upgrade'),
#                     ('shared', 'plus', 'choice_plus', 'upgrade'), ('shared', 'plus', 'pro', 'upgrade'),
#                     ('shared', 'choice_plus', 'pro', 'upgrade'),
#
#                     ('shared', 'plus', 'basic', 'downgrade'), ('shared', 'choice_plus', 'basic', 'downgrade'), ('shared', 'pro', 'basic', 'downgrade'),
#                     ('shared', 'choice_plus', 'plus', 'downgrade'), ('shared', 'pro', 'plus', 'downgrade'),
#                     ('shared', 'pro', 'choice_plus', 'downgrade'),
                      ]

tlds_data = ['com']
payment_method_data = ['check']
domain_name_data = [
                        #'test-inapi-161710617271435800451.com'
                   ]
