
# Library
from dal import autocomplete
from django import forms

# Modules
from . import models
from custom_widgets.multiple_select_list.multiple_select_materialize import MaterializeCheckboxSelectMultiple
from custom_widgets.multiple_autocomplete_select_list.multiple_autocomplete_select import MaterializeModelSelect2Multiple
from custom_widgets.fields.file_field import MaterializeFileInput
from custom_widgets.fields.string_area_field import MaterializeStringAreaField


class BookGenreForm(forms.ModelForm):
    """Book Genre Form Control"""

    class Meta:
        """Meta Book Genre Form"""
        model = models.BookGenres
        fields = [
            'name',
            'description',
            'color'
        ]
    
    def save(self, commit=True, updated=False, **kwargs):
        """Save of Book genre with the form"""
        obj = super(BookGenreForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
        return obj

class AuthorForm(forms.ModelForm):
    """Author Form Control"""

    class Meta:
        """Meta Author Form"""
        model = models.Authors
        fields = [
            "name",
            "image",
            "description",
        ]
        widgets = {
            "description": MaterializeStringAreaField(),
            "image": MaterializeFileInput(),
        }

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Author with the form"""
        obj = super(AuthorForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
            
        return obj
    
class BookForm(autocomplete.FutureModelForm):
    """Book Form Control for Generate Model"""
    genres = forms.ModelMultipleChoiceField(
        queryset=models.BookGenres.objects.filter(enabled=True),
        widget=MaterializeCheckboxSelectMultiple(),
    )
    class Meta:
        """Meta Book Form"""
        model = models.Books
        fields = [
            'name',
            'image',
            'description',
            'authors',
            'genres',
            'file',
        ]
        widgets = {
            "authors": MaterializeModelSelect2Multiple(url="library:author-autocomplete"),
            "image": MaterializeFileInput(),
            "file": MaterializeFileInput(),
        }

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Book with the form"""
        obj = super(BookForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj