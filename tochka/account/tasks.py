from celery import shared_task
from .services import account_balance_subtract


@shared_task
def call_account_balance_subtract(account_uuid):
    account_balance_subtract(account_uuid)
