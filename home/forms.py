"""Forms of Home"""

from django import forms
from . import models
from custom_widgets.multiple_autocomplete_select_list.multiple_autocomplete_select import MaterializeModelSelect2Multiple


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
        widgets = {
            "administrators": MaterializeModelSelect2Multiple(url="accounts:user_autocomplete"),
        }

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Home with the form"""
        obj = super(HomeForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get("user")
        obj.updated_by = kwargs.get("user")

        if commit:
            obj.save()

        return obj