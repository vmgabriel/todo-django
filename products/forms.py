"""Forms of Products"""

# Libraries
from django import forms
from datetime import datetime

# Models
from . import models

class ProductForm(forms.ModelForm):
    """Product Form Control for Generate Model"""
    categories = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.filter(enabled=True),
        widget=forms.CheckboxSelectMultiple()
    )
    class Meta:
        """Meta Board Form"""
        model = models.Product
        fields = [
            'name',
            'description',
            'image',
            'categories',
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(ProductForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj


class CategoryForm(forms.ModelForm):
    """Category Form Control"""

    class Meta:
        """Meta Category Form"""
        model = models.Category
        fields = [
            'name',
            'description',
            'color',
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(CategoryForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
        return obj
