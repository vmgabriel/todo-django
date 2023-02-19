"""Home Models"""

from django.db import models
from django.conf import settings
from location_field.models.plain import PlainLocationField
from versatileimagefield.fields import VersatileImageField, PPOIField
from . import enums


class Home(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    direction = models.CharField(max_length=80)
    location = PlainLocationField(
        based_fields=["city"],
        default=",".join([str(x) for x in settings.INITIAL_LOCATION]),
        zoom=3,
    )
    administrators = models.ManyToManyField("accounts.User", blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        related_name="home_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        related_name="home_updater",
        on_delete=models.CASCADE,
    )


class FloorHome(models.Model):
    number = models.IntegerField()
    plain = VersatileImageField(
        upload_to="images/users",
        ppoi_field="ppoi",
        blank=True,
        verbose_name="image"
    )
    home = models.ForeignKey(
        "home.Home",
        related_name="hf_home",
        on_delete=models.CASCADE
    )
    ppoi = PPOIField(verbose_name="ppoi")
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        related_name="hfloor_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        related_name="hfloor_updater",
        on_delete=models.CASCADE,
    )


class HomeHistory(models.Model):
    home = models.ForeignKey(
        "home.Home",
        related_name="hhistory_home",
        on_delete=models.CASCADE
    )
    note = models.CharField(max_length=100)
    state = models.CharField(
        max_length=40,
        choices=enums.HomeState.choices,
        default=enums.HomeState.INFO,
    )
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User",
        related_name="hhistory_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        related_name="hhistory_updater",
        on_delete=models.CASCADE,
    )


class DepartmentHome(models.Model):
    code = models.CharField(max_length=30)
    home = models.ForeignKey(
        "home.Home",
        related_name="hd_home",
        on_delete=models.CASCADE
    )
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User",
        related_name="hdepartment_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        related_name="hdepartment_updater",
        on_delete=models.CASCADE,
    )


class DepartmentGroupHome(models.Model):
    department = models.ForeignKey(
        "home.DepartmentHome",
        related_name="hdg_department",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "accounts.User",
        related_name="hdg_user",
        on_delete=models.CASCADE
    )
    is_responsible = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User",
        related_name="hdg_creator",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        related_name="hdg_updater",
        on_delete=models.CASCADE,
    )
