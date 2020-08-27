from rest_framework import generics, viewsets

from account.models import Account
from account.serializers import (
    AccountListSerializer,
    AddToBalanceSerializer,
    AccountDetailSerializer
)


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


# class ChangeBalanceViewSet(viewsets.ModelViewSet):
#     """Добавление суммы на баланс счёта абонента"""
#     queryset = Account.objects.filter()
#
#     @action(detail=True, methods=['post'])
#     def add(self, request, *args, **kwargs):
#         serializer_class = AddToBalanceSerializer
#         return Response(self.get_object())
#
#     @action(detail=True, methods=['post'])
#     def subtract(self, request, *args, **kwargs):
#         serializer_class = SubtractBalanceSerializer
