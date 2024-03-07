import pytest, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from tests.bhcore.bhlib.utils.testsetup import testsetup
from tests.bhcore.variables.common import *

predefined_list_of_env_varibales = ['BH_AD_USERNAME_VARIABLE', 'BH_AD_PASSWORD_VARIABLE', 'local', 'env']


@pytest.fixture
def before_test(BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE, local, env):
    print_starred_msg(30, 'Test Setup Started')
    print_msg(BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE)

    testsetupObj = testsetup(local, env, BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE, bh_user='',
                             bh_pswd='Test123!@#')
    admin_user_token = testsetupObj.get_admin_token(testsetupObj)
    print("Admin User Token :" + admin_user_token)

    print_starred_msg(30, 'Test Execution Started')
    yield admin_user_token, testsetupObj

    print_starred_msg(30, 'Test Execution Complete')


def pytest_addoption(parser):
    parser.addoption('--BH_AD_USERNAME_VARIABLE', default=BH_AD_USERNAME_VARIABLE)
    parser.addoption('--BH_AD_PASSWORD_VARIABLE', default=BH_AD_PASSWORD_VARIABLE)
    parser.addoption('--local', default=local)
    parser.addoption('--env', default=env)


def pytest_generate_tests(metafunc):
    metafunc.parametrize(
        'BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE, local, env',
        [(metafunc.config.getoption('BH_AD_USERNAME_VARIABLE'),
          metafunc.config.getoption('BH_AD_PASSWORD_VARIABLE'),
          metafunc.config.getoption('local'),
          metafunc.config.getoption('env'))
         ])


@pytest.fixture
def free_trail_before_test(BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE, local, env):
    print("Test Setup : In-Progress...")
    testsetupObj = testsetup(local, env, BH_AD_USERNAME_VARIABLE, BH_AD_PASSWORD_VARIABLE, bh_user='',
                             bh_pswd='Test123!@#')
    testsetupObj.free_trial = True
    admin_user_token = testsetupObj.get_admin_token(testsetupObj)
    print("Admin User Token :" + admin_user_token)
    yield admin_user_token, testsetupObj
    print("Test Executed. Test Teardown in-Progress...")


def print_msg(*msg):
    print("\n", *msg, "\n")


def print_starred_msg(star_length, *msg):
    stars = '*'
    print("\n\n\n", stars * star_length, "\n", *msg, "\n", stars * star_length, "\n\n\n")
