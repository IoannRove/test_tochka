from rest_framework import serializers
from .models import Account


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
        instance.hold += validated_data.get('hold', 0)
        return instance
