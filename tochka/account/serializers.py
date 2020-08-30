from datetime import datetime, timedelta

from rest_framework import serializers

from .exceptions import HoldOverBalanceException
from .models import Account
from .tasks import call_account_balance_subtract


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('uuid', 'fio', 'status')


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AddToBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('balance',)

    def update(self, instance, validated_data):
        instance.balance += validated_data.get('balance', 0)
        instance.save()
        return instance


class SubtractBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('hold',)

    def update(self, instance, validated_data):
        if instance.balance - instance.hold - validated_data.get('hold', 0) < 0:
            raise HoldOverBalanceException()
        # call_account_balance_subtract.apply_async((instance.uuid,), eta=datetime.utcnow() + timedelta(minutes=10))
        instance.hold += validated_data.get('hold', 0)
        instance.save()
        return instance
