"""Forms to Buy"""

# Libraries
from django import forms
from datetime import datetime

# Models
from . import models, enums
from accounts import models as models_accounts


class ListToBuyForm(forms.ModelForm):
    """Product Form Control for Generate Model"""
    users = forms.ModelMultipleChoiceField(
        queryset=models_accounts.User.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple()
    )
    priority = forms.ChoiceField(choices=enums.Priority.choices)
    class Meta:
        """Meta Board Form"""
        model = models.ListToBuy
        fields = [
            'name',
            'description',
            'priority',
            'users',
        ]

    def __init__(self, user_id: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id:
            self.fields['users'].queryset = queryset=models_accounts.User.objects.filter(is_active=True).exclude(pk=user_id)



    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(ListToBuyForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj


class ItemListToBuyForm(forms.ModelForm):
    class Meta:
        """Meta List Item"""
        model = models.ItemListToBuy
        fields = [
            'list',
            'product',
            'quantity',
        ]

    def __init__(self, list_id: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if list_id:
            self.fields['list'] = forms.ModelChoiceField(label="", widget=forms.HiddenInput(), queryset=None, initial=list_id)
        self.fields["widget"] = widget=forms.HiddenInput()


class ItemListToBuyCompleteForm(forms.ModelForm):
    class Meta:
        """Meta List Item"""
        model = models.ItemListToBuy
        fields = [
            'list',
            'product',
            'quantity',
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Board with the form"""
        obj = super(ItemListToBuyCompleteForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj
