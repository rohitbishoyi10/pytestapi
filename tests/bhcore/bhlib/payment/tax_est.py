import allure

class Tax_Estimate():
    tax_path = '/api/tax_estimate'

    def __init__(self, testsetup):
        self.testsetupObj = testsetup

    @allure.step('Calculate and Retrieve Tax Estimate.')
    def get_tax_json(self, tax_req_dc):
        print("**********\nGET TAX JSON\n*************")
        self.testsetupObj.setHeaders(
            {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
             'Accept': 'application/json, text/javascript, */*; q=0.01'
             })
        headers = self.testsetupObj.getHeaders()

        data = tax_req_dc.json()
        print(data)
        response = self.testsetupObj.mytarget.post(self.tax_path, headers=headers, data=data,
                                                   verify=self.testsetupObj.test_setup_dict['verify_ssl'])
        print("**********\nGET TAX JSON - COMPLETE\n*************")
        try:
            if response.assert_2xx():
                return response.text
            else:
                print('Error Text...')
                print(response.text)
                raise Exception("Unable to calculate Tax, status:" + str(response.status_code))
        except Exception as e:
            print('Caught Exception:' + str(e))
