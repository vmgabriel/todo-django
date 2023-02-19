from django import forms


class MaterializeFileInput(forms.ClearableFileInput):
    template_name = "fields/file.html"