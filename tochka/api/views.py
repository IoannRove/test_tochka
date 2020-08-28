from account.models import Account
from account.serializers import (
    AccountListSerializer,
    AccountDetailSerializer,
    AddToBalanceSerializer,
    SubtractBalanceSerializer,
)
from rest_framework import viewsets


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        elif self.action == 'retrieve':
            return AccountDetailSerializer


class AddSumToBalanceViewSet(viewsets.ModelViewSet):
    """Добавление суммы на баланс счёта абонента"""
    serializer_class = AddToBalanceSerializer
    queryset = Account.objects.filter()


class SubtractBalanceViewSet(viewsets.ModelViewSet):
    """Добавление суммы на баланс счёта абонента"""
    queryset = Account.objects.filter()
    serializer_class = SubtractBalanceSerializer
