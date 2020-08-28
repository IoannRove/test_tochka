from rest_framework.exceptions import APIException


class HoldOverBalanceException(APIException):
    status_code = 400
    default_detail = 'Холд не может превышать баланс счёта абонента.'
    default_code = 'hold_over_balance'


# class NumbersMustBePositive(APIException):
#     status_code = 400
#     default_detail = 'Принимаемый параметр должен быть положительным.'
#     default_code = 'must_be_positive'
