from django.db import models
from django.utils.translation import gettext_lazy


class Registry(models.Model):

    class Meta:
        abstract = True
    
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Plan(Registry):

    class Meta:
        db_table = 'plans'

    class PLAN_TYPE(models.TextChoices):
        BRASS = 'bronze', gettext_lazy('brass')
        SILVER = 'prata', gettext_lazy('silver')
        GOLD = 'ouro', gettext_lazy('gold')
        PLATINUM = 'platina', gettext_lazy('platinum')

    plano = models.CharField(
        max_length=10,
        choices=PLAN_TYPE.choices
    )


class Customer(Registry):

    class Meta:
        db_table = 'customers'

    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    segmento = models.CharField(max_length=100)


class Date(Registry):

    class Meta:
        db_table = 'dates'

    data = models.DateField()
    mes = models.IntegerField()
    ano = models.IntegerField()


class RawPayment(Registry):

    class Meta:
        db_table = 'raw_payments'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text='customer that made the payment'
    ),
    data_pagamento = models.DateField()
    valor = models.FloatField()
    plano = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text='plan related to the payment'
    )
    qtde_meses_pagos = models.IntegerField()
    


class Payment(Registry):

    class Meta:
        db_table = 'payments'
        ordering = ['-updated_at']

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        default=None,
        related_name='payment',
        help_text='customer that made the payment'
    )
    date = models.ForeignKey(
        Date,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text='payment date'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='payment',
        help_text='plan related to the payment'
    )
    valor = models.FloatField()
    qtde_meses_pagos = models.IntegerField()


class MonthlyRecurringRevenue(Registry):

    class Meta:
        db_table = 'monthly_recurring_revenue'
        ordering = ['-updated_at']
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        default=None,
        related_name='monthly recurring revenue',
        help_text='monthly recurring revenue customer'
    )
    mes = models.IntegerField
    ano = models.IntegerField
    recurring_revenue = models.FloatField()


class Test(Registry):

    class Meta:
        db_table = 'tests'
    
    text = models.CharField(max_length=100)
    integer = models.IntegerField()



