"""Lists Forms"""

# Libraries
from django.forms import ModelForm

# Models
from .models import List, Item

class ListForm(ModelForm):
    """List Form Control for Generate Model """
    class Meta:
        """Meta List Form"""
        model = List
        fields = [
            'title',
            'description'
        ]

    def save(self, commit=True, **kwargs):
        """List creation from form"""
        obj = super(ListForm, self).save(commit=False)
        obj.creator = kwargs.get('user')

        if commit:
            obj.save()
        return obj

class ItemForm(ModelForm):
    """Item Form Control for Generate Model """
    class Meta:
        """Meta Item Form"""
        model = Item
        exclude = [
            'created_at',
            'updated_at'
        ]

    def save(self, commit=True, **kwargs):
        """Item creation from form"""
        obj = super(ItemForm, self).save(commit=False)
        obj.responsible_set.clear()
        for resp in self.cleaned_data['responsibles']:
            obj.responsible_set.add(resp)

        if commit:
            obj.save()
        return obj
