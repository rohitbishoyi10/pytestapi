# **********   Module Imports  **************
import allure, pytest
from tests.bhcore.templates.mySite.my_site import mySite_creation
from tests.bhcore.bhlib.dataclasses.template_flows.MySite_Creation import MySite_Creation


# **********   Test Case  **************
@allure.testcase('https://jira.endurance.com/browse/BIQ-296', 'JIRA Link - BIQ 296')
@allure.testcase(
    'https://docs.google.com/spreadsheets/d/1SStrL4iIr2mYAOnDX1XJVntLmePiUiHs3D_Ol3oe9Wk/edit#gid=1052942211',
    'Template Board Link')
@allure.suite('FreeTrial MySite creation Flow')
@allure.title('FreeTrial Account my site creation')
@pytest.mark.skip(reason="This is a test data dependent test case. It will be enabled later on")
def test_mysite_creation_flow(title_tagline_domainName, domain_name, before_test):
    print(domain_name, " | ", title_tagline_domainName[0], " | ", title_tagline_domainName[1])
    admin_user_token, testsetupObj = before_test

    MySite_Creation_Flow_obj = MySite_Creation()
    MySite_Creation_Flow_obj.domain_name = domain_name
    MySite_Creation_Flow_obj.site_title = title_tagline_domainName[0]
    MySite_Creation_Flow_obj.site_tagline = title_tagline_domainName[1]
    MySite_Creation_Flow_obj.site_directory = title_tagline_domainName[2]
    testsetupObj.test_setup_dict['admin_token'] = admin_user_token

    mySite_creation(testsetupObj).my_site_creation_template(MySite_Creation_Flow_obj)


# **********   Test Data Generator  **************
def pytest_generate_tests(metafunc):
    if "domain_name" in metafunc.fixturenames:
        metafunc.parametrize("domain_name", domain_name_data)
    if "title_tagline_domainName" in metafunc.fixturenames:
        metafunc.parametrize("title_tagline_domainName", my_site_creation_data)

# *************   All Test Data (static) below this point  ************

#get domain_name from test_suite_freetrial
domain_name_data = [
                         #'test-inapi-161710617271435800451.com'
                   ]

#my_site_creation_data = [('Hello World 1', 'Welcome','/firstsite'),('Hello World 2', 'Welcome', '/secondmysite')]
my_site_creation_data = [()]
