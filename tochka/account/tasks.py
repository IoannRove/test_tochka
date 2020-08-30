from celery import shared_task

from .services import subtract_account_balance, subtract_all_accounts_balance


@shared_task
def call_account_balance_subtract(account_uuid):
    subtract_account_balance(account_uuid)


@shared_task
def call_subtract_all_accounts_balance():
    subtract_all_accounts_balance()
