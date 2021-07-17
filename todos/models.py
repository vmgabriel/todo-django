"""Models of Todos"""

# Libraries
from django.db import models


class Board(models.Model):
    """Board of Cards"""
    title = models.CharField(max_length=60)
    creator_ref = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)


class Card(models.Model):
    """Card Attribute"""
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=400)
    board_ref = models.ForeignKey(
        'Board',
        on_delete=models.CASCADE,
    )
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "title: {}".format(self.title)
