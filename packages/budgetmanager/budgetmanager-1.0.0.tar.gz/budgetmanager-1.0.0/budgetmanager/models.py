'''
Model classes
'''
# pylint:disable=no-member
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def _get_total_amount(queryset) -> Decimal:
    return queryset.filter(pending=False).aggregate(
        models.Sum('amount', default=0)
    )['amount__sum']


class Budget(models.Model):
    '''
    Model for a budget
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    shared_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BudgetShare',
        related_name='shared_budgets',
        blank=True
    )

    def __str__(self):
        return str(self.name)

    def add_from_csv(self, text: str):
        '''
        Add payees and payments to this budget from a CSV formatted string
        '''
        rows = text.strip().split('\n')
        for line in rows:
            record = line.split(',')
            payee = Payee.objects.get_or_create(
                name=record[0],
                budget=self
            )[0]
            payment = Payment(
                payee=payee,
                amount=record[1],
                date=datetime.strptime(record[2], '%d/%m/%Y'),
            )
            if len(record) >= 4:
                payment.notes = record[3]
            if len(record) >= 5:
                payment.pending = record[4] != ''
            payment.save()

    @property
    def total(self):
        '''The total amount of the Payments of this Budget'''
        return _get_total_amount(Payment.objects.filter(payee__budget=self))

    @classmethod
    def get_user_model(cls):
        return cls._meta.get_field('user').related_model


class BudgetShare(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)

    def clean(self):
        if self.user == self.budget.user:
            raise ValidationError('Budget owner cannot be a shared user')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('budget', 'user'), name='One budget membership per user per budget'),
        ]


class Payee(models.Model):
    '''
    Model for a payee
    '''
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    @property
    def total(self):
        '''
        The total amount of the Payments of this Payee
        '''
        return _get_total_amount(self.payment_set)


class Payment(models.Model):
    '''
    Model for a payment
    Requires a payee and a budget
    Has an amount and date
    '''
    payee = models.ForeignKey(
        Payee,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    date = models.DateField()
    pending = models.BooleanField(
        default=False, verbose_name='Exclude from total')
    notes = models.TextField(null=True, blank=True)

    @classmethod
    def get_total(cls, user):
        '''Get the total amount of the user's Payments'''
        return _get_total_amount(cls.objects.filter(payee_budget__user=user))
