from celery import shared_task

from .tasks_services import subtract_account_balance, subtract_all_accounts_balance


@shared_task
def call_subtract_account_balance(account_uuid):
    """
    Вызывает функцию, которая вычтет значение поля hold из поля balance
    записи таблицы Account с полученным account_uudi.
    :param account_uuid: поле uuid таблицы Account
    :return:
    """
    subtract_account_balance(account_uuid)


@shared_task
def call_subtract_all_accounts_balance():
    """
    Вызывает функцию, которая найдёт все записи таблицы Account и у каждой
    вычтет значение поля hold из поля balance.
    :return:
    """
    subtract_all_accounts_balance()
