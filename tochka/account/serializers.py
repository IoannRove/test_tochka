from rest_framework import serializers

from .exceptions import HoldOverBalanceException
from .models import Account
from .services import add_account_balance, add_account_hold_and_call_subtract_account_balance


class AccountListSerializer(serializers.ModelSerializer):
    """Сериализатор для /account_list. Формирует ответ со всеми полями таблицы Account."""
    class Meta:
        model = Account
        fields = '__all__'


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для /status/<uuid>. Формирует ответ с полями
    balance и status записи с полученным uuid таблицы Account.
    """
    class Meta:
        model = Account
        fields = ('balance', 'status')


class AddToBalanceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для /add/<uuid>. Формирует ответ с результатом сложения
    текущего значения balance и полученным значением.

    Складывает полученное значение с значением balance записи account с указанными uuid
    и сохраняет его в поле balance.
    """
    class Meta:
        model = Account
        fields = ('balance',)

    def update(self, instance, validated_data):
        return add_account_balance(instance, validated_data.get('balance', 0))


class SubtractBalanceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для /subtract/<uuid>. Формирует ответ с результатом сложения
    текущего значения hold и полученным значением.

    Проверят, что сумма полученного значения и текущего значения поля hold
    не превышает значение поля balance записи с указанным uuid.
    Складывает полученное значение с значением hold записи account с указанными uuid
    и сохраняет его в поле hold.
    """
    class Meta:
        model = Account
        fields = ('hold',)

    def update(self, instance, validated_data):
        return add_account_hold_and_call_subtract_account_balance(instance, validated_data.get('hold', 0))
