from bs4 import BeautifulSoup


class payment_receipt():

    exc_description = "Free Trial"
    exc_description_alpha = "Blogs by Bluehost"
    exc_disclaimer = "18004194426"

    def __init__(self, testSetupObj, html):
        self.local = testSetupObj.local
        self.env = testSetupObj.env
        self.html = html

    def validate_receipt_description(self):
        if self.env == 'alpha':
            self.assert_data(self.html, self.exc_description_alpha, 'table', {"class": "items desktop"})
        else:
            self.assert_data(self.html, self.exc_description, 'table', {"class": "items desktop"})


    def validate_receipt_disclaimer(self):
        self.assert_data(self.html, self.exc_disclaimer, 'div', {"class": "success_disclaimer"})

    def assert_data(self, html, exc_str, tag, attribute={}):
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.findAll(tag, attribute)
        find = True
        for results in tags:
            if exc_str in str(results):
                print("data is present in the page")
                find = False
        if find:
            raise Exception(
                "Expected data not found in the page, expected : " + exc_str + "\n actual data : " + str(html))

