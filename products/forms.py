"""Forms of Products"""

# Libraries
from django import forms
from custom_widgets.multiple_select_list.multiple_select_materialize import MaterializeCheckboxSelectMultiple
from custom_widgets.fields.file_field import MaterializeFileInput
from custom_widgets.fields.string_area_field import MaterializeStringAreaField

# Models
from . import models

class ProductForm(forms.ModelForm):
    """Product Form Control for Generate Model"""
    categories = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.filter(enabled=True),
        widget=MaterializeCheckboxSelectMultiple()
    )
    class Meta:
        """Meta Board Form"""
        model = models.Product
        fields = [
            "name",
            "description",
            "image",
            "categories",
        ]
        widgets = {
            "image": MaterializeFileInput(),
            "description": MaterializeStringAreaField(),
        }

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
