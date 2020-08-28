from django.db import transaction

from .models import Account


def account_balance_subtract(account_uuid):
    account = Account.objects.get(pk=account_uuid)

    with transaction.atomic():
        account.balance -= account.hold
        account.hold = 0
        account.save()
