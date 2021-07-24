""" Models related with products management"""

# Libraries
from django.db import models
from djmoney.models.fields import MoneyField

class Store(models.Model):
    """Product Store"""
    title = models.CharField(
        max_length=60,
        blank=False,
        null=False
    )
    description = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=60,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)

class Product(models.Model):
    """Item Product"""
    title = models.CharField(
        max_length=60,
        blank=False,
        null=False
    )
    description = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    brand = models.CharField(
        max_length=60,
        blank=True,
        null=True
    )
    value = MoneyField(
        max_digits=14, 
        decimal_places=2, 
        default_currency='CO'
    )
    store = models.ManyToManyField(
        Store,
        verbose_name="retail store",
        blank=True,
        related_name="retail_store"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)
