from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault
)

from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.Budget.get_user_model()
        fields = ('username', 'first_name', 'last_name')


class BudgetSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.Budget
        fields = ('id', 'name', 'description', 'active', 'user')


class BudgetShareSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.BudgetShare
        fields = ('id', 'budget', 'user')


class PayeeSerializer(ModelSerializer):
    class Meta:
        model = models.Payee
        fields = ('id', 'name', 'description', 'budget')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ('id', 'notes', 'payee', 'amount', 'date', 'pending')
