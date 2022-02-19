"""Store Form"""
# Libraries
from django import forms
from datetime import datetime

# Modules
from . import models


class StoreForm(forms.ModelForm):
    """Store Form Control for Generate Model"""
    class Meta:
        """Meta Board Form"""
        model = models.Store
        fields = [
            'name',
            'description',
            'location',
        ]

    def __init__(self, user = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            if user.home_location:
                self.fields["location"].initial = user.home_location

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(StoreForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        obj.updated_by = kwargs.get('user')
        obj.updated_at = datetime.utcnow()

        if commit:
            obj.save()

        return obj
