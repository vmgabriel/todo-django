"""Library Models"""

# Libraries
from django.db import models

# Modules


class Book(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)