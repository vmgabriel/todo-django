"""Lists Forms"""

# Libraries
from django.forms import ModelForm

# Models
from lists.models.list import List
from lists.models.item import Item

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
        obj.creator = kwargs.get('user')
        obj.item_list = List.objects.get(
            id=kwargs.get('item_list')
        )
        obj.item_responsibles.clear()
        for resp in self.cleaned_data['responsibles']:
            obj.item_responsibles.add(resp)

        if commit:
            obj.save()
        return obj

class ProductForm(ModelForm):
    """Product Form Control for Generate Model """
    class Meta:
        """Meta List Form"""
        model = List
        exclude = [
            'created_at',
            'updated_at'
        ]

    def save(self, commit=True, **kwargs):
        """Product creation from form"""
        obj = super(ProductForm, self).save(commit=False)

        if commit:
            obj.save()
        return obj

class StoreForm(ModelForm):
    """Store Form Control for Generate Model """
    class Meta:
        """Meta List Form"""
        model = List
        exclude = [
            'created_at',
            'updated_at'
        ]

    def save(self, commit=True, **kwargs):
        """Store creation from form"""
        obj = super(StoreForm, self).save(commit=False)

        if commit:
            obj.save()
        return obj