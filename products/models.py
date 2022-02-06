"""Models Products"""

# Libraries
from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.conf import settings
from colorfield.fields import ColorField


class Category(models.Model):
    """Board of Cards"""
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    color = ColorField()

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.name.title())


class Product(models.Model):
    """Board of Cards"""
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    image = VersatileImageField(
        upload_to=f"images",
        blank=True,
        null=True,
    )
    categories = models.ManyToManyField(Category, blank=True)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Product - name: {}".format(self.name)
