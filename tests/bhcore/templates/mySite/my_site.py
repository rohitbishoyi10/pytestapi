from tests.bhcore.bhlib.dataclasses.mycluster.Login import *
from tests.bhcore.bhlib.dataclasses.mycluster.Mysite import Mysite_Creation_DC
from tests.bhcore.bhlib.mycluster.login import login
from tests.bhcore.bhlib.mycluster.my_site_creation import Mysite_Creation


# from ypj_freeTrialMysite.mysite1 import get_user_id


class mySite_creation:
    my_site_creation_flow_dict = {}

    def __init__(self, testsetup):
        self.testSetupObj = testsetup
        self.mysite_creation = Mysite_Creation(self.testSetupObj)
        # self.my_site_creation_flow_dict = copy.deepcopy(testsetup.test_setup_dict)

    def my_site_creation_template(self, MySite_Creation_Flow):
        self.testSetupObj.test_setup_dict['suite.random_domain_name'] = MySite_Creation_Flow.domain_name
        self.domain_name = self.testSetupObj.test_setup_dict['suite.random_domain_name']
        print(self.domain_name)

        self.__loginToAccount()
        # ================================================================================
        # MySite Creation Flow
        # ================================================================================

        # Creation of MySite
        mysite_DC = self.populate_mysite_DC(MySite_Creation_Flow)
        self.__purchase_my_site(mysite_DC)

    def __loginToAccount(self):
        print("\n***************************\nLogin to MyCluster...\n***************************\n")
        loginobj = login(self.testSetupObj)
        my_cluster_login_dc_obj = My_Cluster_Login_DC(bh_account=loginobj.bh_account, bh_password=loginobj.bh_password,
                                                      usession='', my_admin_token='')
        my_cluster_login = loginobj.login_to_my_cluster(my_cluster_login_dc_obj)
        print("\n***************************\nSuccessfully Login to MyCluster...\n***************************\n")

    def __purchase_my_site(self, mysite_DC):
        print("\n***************************\nPurchasing mySite...\n***************************\n")
        return self.mysite_creation.mysite_Creation(mysite_DC)

    def populate_mysite_DC(self, MySite_Creation_Flow):
        mysite_DC = Mysite_Creation_DC()
        if MySite_Creation_Flow.site_title != '' and MySite_Creation_Flow.site_title is not None:
            mysite_DC.title = MySite_Creation_Flow.site_title
        if MySite_Creation_Flow.site_tagline != '' and MySite_Creation_Flow.site_tagline is not None:
            mysite_DC.tagline = MySite_Creation_Flow.site_tagline
        mysite_DC.site_url = "http://" + MySite_Creation_Flow.domain_name + MySite_Creation_Flow.site_directory
        mysite_DC.admin_user_email = self.testSetupObj.bh_ad_user + "@endurance.com"
        return mysite_DC