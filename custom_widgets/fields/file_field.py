from django import forms


class MaterializeFileInput(forms.FileInput):
    template_name = "fields/file.html"