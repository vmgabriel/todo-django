"""Forms for user"""

# Libraries
from django import forms
from versatileimagefield.forms import SizedImageCenterpointClickBootstrap3Field

# Models
from .models import User


class UserForm(forms.ModelForm):
    """User Base Form Related Model"""
    image = SizedImageCenterpointClickBootstrap3Field(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "telephone", "image"]
