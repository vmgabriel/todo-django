
from django.forms import CheckboxSelectMultiple


class MaterializeCheckboxSelectMultiple(CheckboxSelectMultiple):
    input_type = 'checkbox'
    template_name = 'select_multiple_materialize/select.html'
    option_template_name = 'select_multiple_materialize/option.html'