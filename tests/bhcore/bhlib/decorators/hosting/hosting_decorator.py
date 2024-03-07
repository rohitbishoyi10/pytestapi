from tests.bhcore.bhlib.dataclasses.hosting.Hosting import Hosting_DC, Hosting_Payload_DC


class Hosting_Decorator():
    def __init__(self, step_function):
        self.function = step_function

    def __call__(self, Signup_Flow, testsetup_obj, hostingdc):
        # Preprocessing - Decorating
        if testsetup_obj.test_setup_dict['local'] == 'in':
            if testsetup_obj.test_setup_dict['populatefor'] == 'regular':
                hostingdc = self.populate_Hostingdc_BH_IN(testsetup_obj.test_data, Signup_Flow)
            elif testsetup_obj.test_setup_dict['populatefor'] == 'professional_email':
                hostingdc = self.populate_Professional_Email_DC_BH_IN(testsetup_obj.test_data, Signup_Flow)
            else:
                raise Exception ("set the populate for variable in testsetup_obj to decide which method to call for "
                                 "populating data dict.")
        elif testsetup_obj.test_setup_dict['local'] == 'sg':
            if testsetup_obj.test_setup_dict['populatefor'] == 'regular':
                hostingdc = self.populate_Hostingdc_BH_SG(testsetup_obj.test_data, Signup_Flow)
            elif testsetup_obj.test_setup_dict['populatefor'] == 'professional_email':
                hostingdc = self.populate_Professional_Email_DC_BH_SG(testsetup_obj.test_data, Signup_Flow)
            else:
                raise Exception("set the populate for variable in testsetup_obj to decide which method to call for "
                                "populating data dict.")


        data = self.populate_data(hostingdc, testsetup_obj, Signup_Flow)

        # Actual Function Call
        text, custid, domain_name, data_val = self.function(self, Signup_Flow, testsetup_obj, data)

        # Post-processing
        hostingdc.response_html = text
        hostingdc.cust_id = custid
        hostingdc.domain_name = domain_name
        hostingdc.req_data.ir = data['ir']
        if 'flow' in data.keys():
            if data['flow'] is not None:
                hostingdc.req_data.flow = data['flow']
        hostingdc.data_val = data_val

        testsetup_obj.test_setup_dict['suite.random_domain_name'] = domain_name

        return hostingdc

    def split_domain_name(self, domain_name):
        names = domain_name.split('.')
        return names[0], names[1]

    def populate_data(self, hosting_dc, testsetup_obj, Signup_Flow):
        print('creating hosting domain data...')
        data1 = hosting_dc.req_data
        data = data1.dict(exclude_none=True)

        ir_host = 'house^HOMEPAGEBYPASS^' + testsetup_obj.get_host()
        data['ir'] = ir_host + '/web-hosting/signup?' + testsetup_obj.test_data[Signup_Flow.type][Signup_Flow.subtype][
            'plan']

        if hosting_dc.Hosting_Type == 'businessplus' or hosting_dc.Hosting_Type == 'businesspro':
            data['ir'] = ir_host + '/web-hosting/signup?flow=' + testsetup_obj.test_data[Signup_Flow.type][Signup_Flow.subtype][
                             'flow']
            data['flow'] = testsetup_obj.test_data[hosting_dc.Hosting_Type][hosting_dc.Subtype]['flow']

        if hosting_dc.req_data.domain_action == 'register':
            hosting_dc.domain_name = testsetup_obj.create_dynamic_domain()
            name, tld = self.split_domain_name(hosting_dc.domain_name)
            data['domain'] = name
            data['tld'] = tld
        elif hosting_dc.req_data.domain_action == 'transfer':
            hosting_dc.domain_name = testsetup_obj.create_dynamic_domain()
            data['domain'] = hosting_dc.domain_name

        if 'ecom' in hosting_dc.Hosting_Type.lower():
            data['flow'] = 'woocommerce'
            data['ir'] = ir_host + '/web-hosting/signup?flow=woocommerce&' + \
                         testsetup_obj.test_data[Signup_Flow.type][Signup_Flow.subtype]['plan']

        if Signup_Flow.affiliates:
            data['ir'] = data1.dict(exclude_none=True)['ir']

        return data

    # ================================================================================
    #                       INDIA - Populate Data
    # ================================================================================

    def populate_Hostingdc_BH_IN(self, testsetup_dict, Signup_Flow):
        hostingdc = Hosting_DC()
        hosting_req_dc = Hosting_Payload_DC()
        # hosting_req_dc.ir_host = ''
        hosting_req_dc.domain_action = Signup_Flow.domain_type
        hosting_req_dc.currency = 'INR'
        hosting_req_dc.c = ''
        hosting_req_dc.sku = testsetup_dict[Signup_Flow.type][Signup_Flow.subtype]['sku']
        # hosting_req_dc.flow = testsetup_dict[Signup_Flow.type][Signup_Flow.subtype]['flow']
        hosting_req_dc.show_header = ''
        if Signup_Flow.affiliates:
            hosting_req_dc.no_cookie_brick = 'on'
            hosting_req_dc.ir = Signup_Flow.ir
        hostingdc.req_data = hosting_req_dc
        return hostingdc

    def populate_FreeTrial_DC_BH_IN(self, testsetup_dict, Free_Trial):
        hostingdc = Hosting_DC()
        # hostingdc.domain_action = Free_Trail.domain_type
        hostingdc.Hosting_Type = Free_Trial.type
        hostingdc.Subtype = Free_Trial.subtype

        hosting_req_dc = Hosting_Payload_DC()
        # hosting_req_dc.ir_host = ''
        hosting_req_dc.domain_action = Free_Trial.domain_type
        hosting_req_dc.currency = 'INR'
        hosting_req_dc.c = ''
        hosting_req_dc.sku = ''
        hosting_req_dc.show_header = ''

        hostingdc.req_data = hosting_req_dc
        return hostingdc

    def populate_Professional_Email_DC_BH_IN(self, testsetup_dict, Pro_Email_Flow):
        hostingdc = Hosting_DC()
        hostingdc.Hosting_Type = Pro_Email_Flow.type
        hostingdc.Subtype = Pro_Email_Flow.subtype
        hosting_req_dc = Hosting_Payload_DC()
        hosting_req_dc.domain_action = Pro_Email_Flow.domain_type
        hosting_req_dc.currency = 'INR'
        hosting_req_dc.c = ''
        hosting_req_dc.sku = testsetup_dict[Pro_Email_Flow.type][Pro_Email_Flow.subtype]['sku']
        hosting_req_dc.show_header = ''
        # hosting_req_dc.flow = Pro_Email_Flow.flow
        # hosting_req_dc.ir_host = ''
        if Pro_Email_Flow.affiliates:
            hosting_req_dc.no_cookie_brick = 'on'
            hosting_req_dc.ir = Pro_Email_Flow.ir
        hostingdc.req_data = hosting_req_dc
        return hostingdc

    # ================================================================================
    #                       SINGAPORE - Populate Data
    # ================================================================================

    def populate_Hostingdc_BH_SG(self, testsetup_dict, Signup_Flow):
        hostingdc = Hosting_DC()
        hostingdc.Hosting_Type = Signup_Flow.type
        hostingdc.Subtype = Signup_Flow.subtype

        hosting_req_dc = Hosting_Payload_DC()
        hosting_req_dc.domain_action = Signup_Flow.domain_type
        hosting_req_dc.currency = 'SGD'
        hosting_req_dc.c = ''
        # hosting_req_dc.sku = testsetup_dict[Signup_Flow.type][Signup_Flow.subtype]['sku_sg']
        hosting_req_dc.sku = testsetup_dict[Signup_Flow.type][Signup_Flow.subtype]['sku']
        hosting_req_dc.show_header = ''
        # hosting_req_dc.ir_host = ''
        if Signup_Flow.affiliates:
            hosting_req_dc.no_cookie_brick = 'on'
            hosting_req_dc.ir = Signup_Flow.ir
        hostingdc.req_data = hosting_req_dc
        return hostingdc

    def populate_Professional_Email_DC_BH_SG(self, testsetup_dict, Pro_Email_Flow):
        hostingdc = Hosting_DC()
        hostingdc.Hosting_Type = Pro_Email_Flow.type
        hostingdc.Subtype = Pro_Email_Flow.subtype
        hosting_req_dc = Hosting_Payload_DC()
        hosting_req_dc.domain_action = Pro_Email_Flow.domain_type
        hosting_req_dc.currency = 'INR'
        hosting_req_dc.c = ''
        hosting_req_dc.sku = testsetup_dict[Pro_Email_Flow.type][Pro_Email_Flow.subtype]['sku']
        hosting_req_dc.show_header = ''
        # hosting_req_dc.flow = Pro_Email_Flow.flow
        # hosting_req_dc.ir_host = ''
        if Pro_Email_Flow.affiliates:
            hosting_req_dc.no_cookie_brick = 'on'
            hosting_req_dc.ir = Pro_Email_Flow.ir
        hostingdc.req_data = hosting_req_dc
        return hostingdc