"""Models to buy"""

# Libraries
from django.db import models

# Modules
from . import enums


class ListToBuy(models.Model):
    """List to buy data components"""
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    priority = models.CharField(
        max_length=40,
        choices=enums.Priority.choices,
        default=enums.Priority.LOW
    )
    users = models.ManyToManyField(
        'accounts.User',
        related_name="stackeholders",
    )

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name="creator"
    )

    def __str__(self):
        return "{}".format(str(self.name).title())


class ItemListToBuy(models.Model):
    """Relation of List and Product"""
    list = models.ForeignKey(
        ListToBuy,
        on_delete=models.CASCADE,
        #related_name='list'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        #related_name='product',
    )
    quantity = models.PositiveIntegerField(default=1)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        #related_name="creator"
    )

    def __str__(self):
        return "{}".format(str(self.list.name).title())
