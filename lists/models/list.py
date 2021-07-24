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
        'accounts.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)
