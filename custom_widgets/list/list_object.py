from typing import Union
from custom_widgets import fields


class ListComponent:
    name: str
    to_show: str
    field: Union[fields.Field, None]
    custom_widgets: fields.abstracts.WidgetList

    def __init__(self, name: str, to_show: str, widget: fields.Field = None, custom_widget: fields.abstracts.WidgetList = None):
        self.name = name
        self.to_show = to_show
        self.widget = widget or fields.Field.STRING
        self.custom_widget = custom_widget or fields.get_field_list(self.widget)()