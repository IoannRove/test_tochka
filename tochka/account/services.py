from datetime import datetime, timedelta

from .exceptions import HoldOverBalanceException
from .tasks import call_subtract_account_balance


def add_account_balance(account, balance):
    """
    Добавляет значение balance к значению поля balance записи account.
    :param account: запись таблицы Account
    :param balance: принятый баланс
    :return: account
    """
    account.balance += balance
    account.save()
    return account


def is_possible_add_account_hold(account, result_hold):
    """
    Проверяет возможно ли добавление принятого значения к текущему значению поля hold.
    Для этого необходимо, чтобы их сумма была меньше или равна текущему балансу.
    :param account: запись таблицы Account
    :param result_hold: сумма принятого значения и текущего значения поля hold записи account
    :return: Boolean
    """
    return account.balance - result_hold >= 0


def add_account_hold(account, hold):
    """
    При возможности добавляет полученное значение hold к полю hold записи account.
    Проверяется возможность операции - баланс должен быть
    больше или равен сумме полученного значения и текущего значения hold.
    При невозможости рэйзится ошибка. В обратном случае, сумма записывается в поле hold записи account.
    :param account: запись таблицы Account
    :param hold: полученное значение hold
    :return: None or account
    """
    result_hold = account.hold + hold
    if is_possible_add_account_hold(account, result_hold):
        account.hold = result_hold
        account.save()
        return account
    raise HoldOverBalanceException()


def add_account_hold_and_call_subtract_account_balance(account, hold):
    """
    Вызывает add_account_hold, которая добавляет полученный hold к полю hold записи account и
    создаёт таск для celery subtract_account_balance, который начнёт выполнятся через 10 минут и
    вычтет значение поля hold из поля balance.
    :param account: запись таблицы Account
    :param hold: полученный холд
    :return: account
    """
    account = add_account_hold(account, hold)
    call_subtract_account_balance.apply_async((account.uuid,), eta=datetime.utcnow() + timedelta(minutes=10))
    return account
