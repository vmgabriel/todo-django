"""Store Models"""

# Libraries
from location_field.models.plain import PlainLocationField
from djmoney.models.fields import MoneyField
from django.db import models
from django.conf import settings


class Store(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    location = PlainLocationField(
        based_fields=['city'],
        default=",".join([str(x) for x in settings.INITIAL_LOCATION]),
        zoom=3,
    )

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        related_name="store_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        related_name="store_updater",
        on_delete=models.CASCADE,
    )


class StoreProduct(models.Model):
    store = models.ForeignKey(
        "stores.Store",
        related_name="sp_store",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product",
        related_name="sp_product",
        on_delete=models.CASCADE
    )

    description = models.CharField(max_length=120)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        related_name="sp_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        related_name="sp_updater",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} - ${}".format(str(self.store.name).title(), self.price)
