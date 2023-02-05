"""Autocomplete of Materialize Adapt"""

from dal import autocomplete
from django import forms

class MaterializeModelSelect2Multiple(autocomplete.ModelSelect2Multiple):
    template_name = 'autocomplete_multiple_select/select.html'
    option_template_name = 'autocomplete_multiple_select/option.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def media(self):
        to_include_css = "css/custom_select.css"
        result = super().media

        list_css = result._css_lists
        to_modify_dict = list_css[0]
        to_modify_dict["screen"] = (*to_modify_dict["screen"], to_include_css)
        return result