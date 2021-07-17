""" Models of Lists"""

# Libraries
from django.db import models

class List(models.Model):
    """Item List"""
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
    creator = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)

class Item(models.Model):
    """List Items"""
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
    check = models.BooleanField(
        "Item completed",
        default=False
    )
    value = models.DecimalField(
        max_digits=16,
        decimal_places=4,
        default=0
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )
    creator = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    responsible = models.ManyToManyField(
        'auth.User',
        verbose_name="responsibles related",
        blank=True,
        related_name="item_responsabilities"
    )
    item_list = models.ForeignKey(
        List,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)
