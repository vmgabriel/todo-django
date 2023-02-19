"""Forms of Home"""

from django import forms
from . import models

class HomeForm(forms.ModelForm):
    """Home Form Control"""

    class Meta:
        """Meta Home Form"""
        model = models.Home
        fields = [
            "name",
            "description",
            "direction",
            "location",
            "administrators",
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Home with the form"""
        obj = super(HomeForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get("user")
        obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj