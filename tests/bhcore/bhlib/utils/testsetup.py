import yaml, threading
from tests.bhcore.bhlib.utils.apiritif.http import *
from tests.bhcore.bhlib.webcluster.cgi.signup import signup
import random


class testsetup():
    cookies = {}
    basic_cookies = {}
    headers = {'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                         '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    host = ''
    my_host = ''
    i_host = ''
    bh_ad_user = ''
    bh_ad_pswd = ''
    bh_user = ''
    bh_pswd = 'Test123!@#'
    verify_ssl = True
    free_trial = False
    test_setup_dict = {}
    test_data = {}

    def __init__(self, local, env, bh_ad_user, bh_ad_pswd, bh_user='', bh_pswd=''):
        self.headers = copy.deepcopy(self.headers)
        self.test_setup_dict['local'] = local
        self.test_setup_dict['env'] = env
        self.local = local
        self.env = env
        self.bh_ad_user = bh_ad_user
        self.bh_ad_pswd = bh_ad_pswd
        self.bh_user = bh_user
        self.bh_pswd = bh_pswd
        self.config_yaml_path = os.path.abspath(os.getcwd() + "/tests/bhcore/variables/config.yaml")
        self.test_data_yaml_path = os.path.abspath(os.getcwd() + "/tests/bhcore/variables/test_data.yaml")
        self.setup_request_details(self.config_yaml_path, local, env)
        self.__load_hosting_test_data(self.test_data_yaml_path)
        self.target = http.target(self.get_host())
        self.mytarget = http.target(self.get_myhost())
        self.itarget = http.target(self.get_ihost())
        self.timeStampLock = threading.Lock()
        self.is_verify_ssl()

    def setup_request_details(self, yaml_file, local, env):
        with open(yaml_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.cookies = data['cookies'][local]
            self.cookies['alert-box'] = 'open'
            self.basic_cookies = copy.deepcopy(self.cookies)

            self.headers.update(data['headers'][local])
            if 'alpha' in self.env.lower():
                self.verify_ssl = False
                if 'alpha_user' in os.environ:
                    alpha_user = os.environ['alpha_user']
                    if alpha_user:
                        self.set_host('https://www.' + alpha_user + '.alpha.bluehost.in')
                        self.set_myhost('https://my.' + alpha_user + '.alpha.bluehost.in')
                    else:
                        self.set_host(data['environments'][local][env]['host_server'])
                        self.set_myhost(data['environments'][local][env]['my_host_server'])
            else:
                self.__set_host(data['environments'][local][env]['host_server'])
                self.__set_myhost(data['environments'][local][env]['my_host_server'])
                self.__set_ihost(data['environments'][local][env]['i_host_server'])

    def is_verify_ssl(self):
        if self.local == 'sg':
            self.verify_ssl = False
        self.test_setup_dict['verify_ssl'] = self.verify_ssl
        return self.verify_ssl

    def __set_host(self, host):
        self.test_setup_dict['host'] = host
        self.host = host

    def get_host(self):
        return self.host

    def __set_myhost(self, my_host):
        self.test_setup_dict['my_host'] = my_host
        self.my_host = my_host

    def get_myhost(self):
        return self.my_host

    def __set_ihost(self, i_host):
        self.test_setup_dict['i_host'] = i_host
        self.i_host = i_host

    def get_ihost(self):
        return self.i_host

    def setCookies(self, extra_cookies, remove_cookies=None):
        if extra_cookies is not None:
            for h in extra_cookies:
                self.cookies.update([(h, extra_cookies[h])])
        if remove_cookies is not None:
            for h in remove_cookies:
                self.cookies.pop(h)
        self.test_setup_dict['cookies'] = self.cookies

    def getCookies(self):
        return self.cookies

    def resetCookies(self):
        self.cookies = self.basic_cookies

    def setHeaders(self, extra_headers, remove_headers=None):
        if extra_headers is not None:
            for h in extra_headers:
                self.headers.update([(h, extra_headers[h])])
        if remove_headers is not None:
            for h in remove_headers:
                self.headers.pop(h)

        self.test_setup_dict['headers'] = self.headers

    def getHeaders(self):
        return self.headers

    def __load_hosting_test_data(self, test_data_yaml_file):
        with open(test_data_yaml_file) as f:
            self.test_data = yaml.load(f, Loader=yaml.FullLoader)

    # def populate_hosting_test_data(self, hosting_type, subtype):
    def populate_hosting_test_data(self,signup_flow_dc ):
        if signup_flow_dc.type == 'freetrial':
            self.test_setup_dict['term'] = self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['TERM']
        else:
            self.test_setup_dict['term']=signup_flow_dc.term
        if signup_flow_dc.price_flag:
            if self.local=='in':
                if signup_flow_dc.domain_type=='register':
                    self.test_setup_dict['price'] = self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][0][0]
                elif signup_flow_dc.domain_type=="domainless":
                    self.test_setup_dict['price']=self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][0][1]
                else:
                    self.test_setup_dict['price']=self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][0][2]

            else:
                if signup_flow_dc.domain_type == 'register':
                    self.test_setup_dict['price'] = self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][1][0]
                elif signup_flow_dc.domain_type == "domainless":
                    self.test_setup_dict['price'] = self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][1][1]
                else:
                    self.test_setup_dict['price'] = self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['price'][signup_flow_dc.term][1][2]

        self.sku=self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['sku']
        self.plans=self.test_data[signup_flow_dc.type][signup_flow_dc.subtype]['plan']
        self.test_setup_dict['sku'] = self.sku
        self.test_setup_dict['plans'] = self.plans

        return self.sku, self.plans

    def create_dynamic_domain(self):
        self.timeStampLock.acquire()
        # timestamp = int(round(time.time_ns()))
        timestamp = int(time.time() * 1000000)
        time.sleep(.001)
        self.timeStampLock.release()
        random_domain_name = 'test-' + self.local + 'api-' + str(timestamp) + f'{random.randrange(1, 10 ** 3):05}' + \
                             '.' + self.test_setup_dict['tld']
        self.test_setup_dict['suite.random_domain_name'] = random_domain_name
        print('Domain Name Created :'+ self.test_setup_dict['suite.random_domain_name'])
        return random_domain_name

    def get_admin_token(self, testsetup):
        admin_token = signup(testsetup).get_admin_user_token()
        self.setCookies({'admin_user': admin_token})
        self.test_setup_dict['admin_token'] = admin_token
        return admin_token

    def get_expired_admin_token(self):
        admin_token = ''
        return admin_token

    def get_empty_admin_token(self):
        admin_token = ''
        return admin_token

    def get_null_admin_token(self):
        admin_token = None
        return admin_token

# testsetup = testsetup('in', 'alpha')
# print(testsetup.test_setup_dict)
# print(testsetup.test_data)
