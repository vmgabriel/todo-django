"""Models of account"""

# Libraries
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from location_field.models.plain import PlainLocationField

# Modules
from versatileimagefield.fields import VersatileImageField, PPOIField


class UserManager(BaseUserManager):
    """Creation of User - Manager"""
    def create_user(
            self,
            email=None,
            password=None,
            first_name=None,
            last_name=None,
            is_staff=None,
            is_active=None,
            telephone=None,
            groups=None,
            **kwargs
    ):
        """Create User"""
        email = UserManager.normalize_email(email.lower())
        user = self.model(
            email=email,
            is_active=is_active or True,
            first_name=first_name,
            telephone=telephone,
            is_staff=is_staff,
            **kwargs
        )
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
        if groups:
            user.groups = groups
        user.save()
        return user

    def create_superuser(
            self, email, username, password=None, first_name=None, last_name=None, groups=None, **kwargs
    ):
        """Creation of superuser"""
        return self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            groups=groups,
            username=username,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )


class User(PermissionsMixin, AbstractBaseUser):
    """User Main Model"""
    email = models.EmailField("Email", unique=True)
    username = models.CharField("Username", unique=True, max_length=128)
    first_name = models.CharField("First Name", max_length=256)
    last_name = models.CharField("Last Name", max_length=256, blank=True)
    is_staff = models.BooleanField("Staff Status", default=False)
    is_active = models.BooleanField("IS Active", default=True)
    date_joined = models.DateTimeField("Date Joined", default=timezone.now, editable=False)
    telephone = models.CharField("Phone Number", max_length=30, blank=True, null=True)
    blocked_at = models.DateTimeField(blank=True, null=True)
    language_code = models.CharField(max_length=10, default=settings.LANGUAGE_CODE)
    image = VersatileImageField(
        upload_to="images/users",
        ppoi_field="ppoi",
        blank=True,
        verbose_name="image"
    )
    ppoi = PPOIField(verbose_name="ppoi")
    groups = models.ManyToManyField(Group, verbose_name="Groups", related_name="user_groups", blank=True)
    home_location = PlainLocationField(
        based_fields=['city'],
        default=",".join([str(x) for x in settings.INITIAL_LOCATION]),
        zoom=3,
        null=True,
    )
    wallet = MoneyField(
        default_currency=settings.DEFAULT_CURRENCIES[0],
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    alkali = MoneyField(
        default_currency=settings.DEFAULT_CURRENCIES[0],
        max_digits=11,
        decimal_places=2,
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "telephone", "username"]

    class Meta:
        """Meta Class Intern"""
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def add_to_wallet(self, value: Money, is_plus: bool = True):
        if self.wallet is None:
            self.wallet = Money(0, value.currency)
        if is_plus:
            self.wallet += value
        else:
            self.wallet -= value

    def add_to_alkali(self, value: Money, is_plus: bool = True):
        if self.is_plus is None:
            self.is_plus = Money(0, value.currency)
        if is_plus:
            self.alkali += value
        else:
            self.alkali -= value
