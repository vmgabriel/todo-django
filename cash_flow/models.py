"""Models configuration for cash flow"""

# Libraries
from datetime import datetime
from colorfield.fields import ColorField
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from djmoney.money import Money


class TypeFlow(models.TextChoices):
    EXPENDITURE = 'E', _('Expenditure')
    INCOME = 'I', _('Income')

class StateFlow(models.TextChoices):
    ACTIVE = "A", _("Active")
    PASSIVE = "P", _("Passive")


class CategoryFlow(models.Model):
    """Categories of CashFlow"""
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    color = ColorField()
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    type_flow = models.CharField(max_length=3, choices=TypeFlow.choices)
    state_flow = models.CharField(max_length=3, choices=StateFlow.choices, blank=True, null=True)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.name)


class FlowMoney(models.Model):
    """Flow Money"""
    description = models.CharField(max_length=80)
    category = models.ForeignKey(CategoryFlow, on_delete=models.CASCADE)
    amount = MoneyField(
        default_currency=settings.DEFAULT_CURRENCIES[0],
        max_digits=11,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date_flow = models.DateTimeField(default=datetime.now())

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    @property
    def abs_amount(self) -> Money:
        return abs(self.amount)