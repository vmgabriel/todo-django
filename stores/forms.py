"""Store Form"""

# Libraries
from django import forms
from datetime import datetime
from django.conf import settings
from djmoney.models.fields import MoneyField

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

class StoreProductForm(forms.ModelForm):
    """Store Product Control"""

    class Meta:
        """Meta Store Product Form"""
        model = models.StoreProduct
        fields = [
            "store",
            "product",
            "price",
            "description",
        ]

    price = MoneyField(
        max_digits=10,
        decimal_places=2
    )

    def __init__(self, store_id: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if store_id:
            self.fields['store'] = forms.ModelChoiceField(
                label="",
                widget=forms.HiddenInput(),
                queryset=None,
                initial=store_id
            )
        self.fields["widget"] = forms.HiddenInput()


class StoreProductCompleteForm(forms.ModelForm):
    class Meta:
        """Meta Store Product Complete"""
        model = models.StoreProduct
        fields = [
            "store",
            "product",
            "description",
            "price",
        ]

    price = MoneyField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(StoreProductCompleteForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        obj.updated_by = kwargs.get('user')
        obj.updated_at = datetime.utcnow()

        if commit:
            obj.save()

        return obj

