
# Library
from django import forms

# Modules
from . import models

class BookGenreForm(forms.ModelForm):
    "Book Genre Form Control"

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
    "Author Form Control"

    class Meta:
        """Meta Author Form"""
        model = models.Authors
        fields = [
            'name',
            'image',
            'description',
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Author with the form"""
        obj = super(AuthorForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
            
        return obj
    
class BookForm(forms.ModelForm):
    """Book Form Control for Generate Model"""
    genres = forms.ModelMultipleChoiceField(
        queryset=models.BookGenres.objects.filter(enabled=True),
        widget=forms.CheckboxSelectMultiple()
    )
    authors = forms.ModelMultipleChoiceField(
        queryset=models.Authors.objects.filter(enabled=True),
        widget=forms.CheckboxSelectMultiple()
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

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Book with the form"""
        obj = super(BookForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        #obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()

        return obj