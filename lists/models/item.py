""" Models of Items"""

# Libraries
from django.db import models

# Models
from lists.models.list import List

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
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )
    quantity = models.IntegerField(
        default=0,
        null=False
    )
    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    responsible = models.ManyToManyField(
        'accounts.User',
        verbose_name="responsibles related",
        blank=True,
        related_name="item_responsibles"
    )
    item_list = models.ForeignKey(
        List,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)
