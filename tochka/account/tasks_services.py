from django.db import transaction

from .models import Account


def subtract_balance(account):
    """
    Вычитает из значения поля balance значение поля hold,
    обнуляет значение поля hold и сохраняет запись account
    :param account: запись таблицы Account
    :return:
    """
    with transaction.atomic():
        account.balance -= account.hold
        account.hold = 0
        account.save()


def subtract_account_balance(account_uuid):
    """
    Находит запись account по полученному account_uuid и
    вызывает функцию subtract_balance с account в качестве параметра,
    которая вычитает холд из баланса счёта.
    :param account_uuid: поле uuid таблицы Account
    :return:
    """
    account = Account.objects.get(pk=account_uuid)
    subtract_balance(account)


def subtract_all_accounts_balance():
    """
    Находит все записи таблицы Account и вызывает subtract_balance
    с параметром account - элемент списка accounts,
    которая вычитает холд из баланса счёта.
    :return:
    """
    accounts = Account.objects.all()

    for account in accounts:
        subtract_balance(account)
