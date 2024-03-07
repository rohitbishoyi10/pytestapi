from bs4 import BeautifulSoup

class create_account():
    exc_trial_title = "Start Your Free Trial for Bluehost Hosting"
    exc_free_trial_plan_package = "Your Free Trial Plan package includes"
    exc_extra_package = "Domain Privacy + Protection"
    exc_disclaimer = "18004194426"
    exc_pay_option = "Pay by Credit / Debit Card"
    exc_pay_msg = "A temporary authorization fee of ₹2 might be charged to verify your card. It will be refunded immediately"
    exc_domain_registration = "Primary Domain Registration"

    def __init__(self, html):
        self.html = html


    def validate_free_trial_title(self):
        self.assert_data(self.html, self.exc_trial_title, 'span', {"class": "stitle"})

    def validate_free_trial_plan_package(self):
        self.assert_data(self.html, self.exc_free_trial_plan_package, 'div', {"class": "free_trial_right"})

    def validate_extra_package(self):
        self.assert_data(self.html, self.exc_extra_package, 'label', {"class": "signuplabel"})

    def validate_domain_registration(self):
        self.assert_data(self.html, self.exc_domain_registration, 'span', {"class": "signuplabel"})

    def validate_pay_option(self):
        self.assert_data(self.html, self.exc_pay_option, 'label', {"for": "paymethod_cc"})

    def validate_pay_msg(self):
        self.assert_data(self.html, self.exc_pay_msg, 'div', {"id":"billing_info"})

    def validate_disclaimer(self):
        self.assert_data(self.html, self.exc_disclaimer, 'div', {"id": "disclaimer-copy"})

    def assert_data(self, html, exc_str, tag, attribute ={}):
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.findAll(tag, attribute)
        find = True
        for results in tags:
            if exc_str in str(results):
                print("data is present in the page")
                find = False
        if find:
            raise Exception("Expected data not found in the page, expected : " + exc_str +"\n actual data : " + str(html))
