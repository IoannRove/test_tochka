from django.db import transaction

from .models import Account


def subtract_account_balance(account_uuid):
    account = Account.objects.get(pk=account_uuid)

    with transaction.atomic():
        account.balance -= account.hold
        account.hold = 0
        account.save()


def subtract_all_accounts_balance():
    accounts = Account.objects.all()

    for account in accounts:
        with transaction.atomic():
            account.balance -= account.hold
            account.hold = 0
            account.save()
