"""All Enums of System"""

# Libraries
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum


class Priority(models.TextChoices):
    HIGH = "high", _("High")
    MEDIUM = "medium", _("Medium")
    LOW = "low", _("Low")
