
# Library
from django import forms

# Modules
from . import models

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

    class Meta:
        """Meta Category Form"""
        model = models.Book
        fields = [
        ]