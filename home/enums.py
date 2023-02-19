"""Home Enums"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class HomeState(models.TextChoices):
    INFO = "info", _("Info")
    FIX = "fix", _("Fix")
    FIXED = "fixed", _("Fixed")