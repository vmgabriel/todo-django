"""Models of Socials"""

from django.db import models
from django.conf import settings

from . import SocialIntegration


class SocialConnection(models.Model):
    """Integration with other social connections"""
    social_connect = models.CharField(
        max_length=40,
        choices=SocialIntegration.CHOICES,
        default=SocialIntegration.SPOTIFY
    )
    code = models.CharField(
        "code",
        max_length=70
    )
    access_token = models.CharField(
        "access_token",
        max_length=120,
        null=True,
    )
    refresh_token = models.CharField(
        "refresh_token",
        max_length=120,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
