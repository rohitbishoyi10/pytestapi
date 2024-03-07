# **********   Module Imports  **************
from tests.bhcore.templates.singnup_flow.signup_flow import signup_flow
from tests.bhcore.bhlib.dataclasses.template_flows.Signup_Flow import *
import pytest

# **********   Test Case  **************
def test_hosting_parmeterized_flow_with_GST(hosting_plans, domain_action, payment_method, tlds, gst_id, before_test):
    print(hosting_plans[0], hosting_plans[1], " | ", domain_action, " | ", tlds, " | ", payment_method)

    admin_user_token, testsetupObj = before_test
    testsetupObj.test_setup_dict['populatefor'] = 'regular'

    testsetupObj.test_setup_dict['admin_token'] = admin_user_token
    testsetupObj.test_setup_dict['tld'] = tlds
    testsetupObj.test_setup_dict['Hosting_Type'] = hosting_plans[0]
    testsetupObj.test_setup_dict['Subtype'] = hosting_plans[1]

    signup_flow_obj = Signup_Flow()
    signup_flow_obj.type = hosting_plans[0]
    signup_flow_obj.subtype = hosting_plans[1]
    signup_flow_obj.domain_type = domain_action
    signup_flow_obj.payment_type = payment_method
    signup_flow_obj.tax_id = gst_id

    signup_flow(testsetupObj).signup_template_invalid_gst(signup_flow_obj)


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
    if "gst_id" in metafunc.fixturenames:
        metafunc.parametrize("gst_id", gst_id_data)


# *************   All Test Data (static) below this point  ************

# All Hosting Type and Sub Type combos
shared_hosting_plans = [('shared', 'plus'), ('shared', 'pro'), ('shared', 'choice_plus')]
ecom_hosting_plans = [('ecom', 'starter')]
wppro_hosting_plans = [('wppro', 'build')]
# vps_hosting_plans = [('vps', 'standard'), ('vps', 'enhanced'), ('vps', 'ultimate')]
# dedicated_hosting_plans = [('dedicated', 'standard'), ('dedicated', 'enhanced'), ('dedicated', 'premium')]

# hosting_plans_data = [*shared_hosting_plans, *wppro_hosting_plans, *ecom_hosting_plans, *vps_hosting_plans, *dedicated_hosting_plans ]
# hosting_term_data = [1, 2, 3]
hosting_plans_data = [*shared_hosting_plans, *wppro_hosting_plans, *ecom_hosting_plans]
tlds_data = ['com']
payment_method_data = ['check']
domain_action_data = ['register', 'transfer', 'domainless']
gst_id_data = ['27AADCB2230M1ZT']
