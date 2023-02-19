
from django import forms


class MaterializeStringAreaField(forms.Textarea):
    template_name = "fields/string_area.html"
