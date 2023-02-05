from django import forms


class MaterializeFileInput(forms.FileInput):
    template_name = "file/file.html"