"""Store Models"""

# Libraries
from location_field.models.plain import PlainLocationField
from django_admin_geomap import GeoItem
from django.db import models
from django.conf import settings


class Store(models.Model, GeoItem):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    location = PlainLocationField(
        based_fields=['city'],
        default=",".join([str(x) for x in settings.INITIAL_LOCATION]),
        zoom=3,
    )

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        related_name="store_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        related_name="store_updater",
        on_delete=models.CASCADE,
    )
