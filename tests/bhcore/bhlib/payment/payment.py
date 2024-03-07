from tests.bhcore.bhlib.payment.check import *

class payment():
    def __init__(self, testsetup_obj):
        self.testsetup_obj = testsetup_obj

    def pay(self, Paymentdc_obj):
        payer = self._get_payer(Paymentdc_obj)
        return payer

    def _get_payer(self, Paymentdc_obj):
        if Paymentdc_obj.paymethod == 'check':
            return self._pay_by_check(Paymentdc_obj)
        elif Paymentdc_obj.paymethod == 'worldpay':
            return self._pay_by_worldpay()
        elif Paymentdc_obj.paymethod == 'payubiz':
            return self._pay_by_payubiz()
        else:
            raise ValueError(Paymentdc_obj.payment_type)

    @allure.step('Validation of Payment process via Check.')
    def _pay_by_check(self, Paymentdc_obj):
        check_payment = check(self.testsetup_obj)
        return check_payment.pay_by_check(Paymentdc_obj)

    def _pay_by_worldpay(self):
        pass

    def _pay_by_payubiz(self):
        pass
