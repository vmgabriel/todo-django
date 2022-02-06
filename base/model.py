
# Libraries
from django.db import models

class MetaModel(models.Model):
    """MetaModel"""
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )
