"""Forms for user"""

# Libraries
from django import forms
from versatileimagefield.forms import SizedImageCenterpointClickBootstrap3Field
from django.contrib.auth.forms import UserCreationForm

# Models
from .models import User


class RegisterForm(UserCreationForm):
    """Register Form"""
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")

    def save(self, commit=True, **kwargs):
        obj = super(RegisterForm, self).save(commit=False)

        if commit:
            obj.save()

        return obj


class UserForm(forms.ModelForm):
    """User Base Form Related Model"""
    image = SizedImageCenterpointClickBootstrap3Field(required=False)

    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "telephone", "image"
        ]
