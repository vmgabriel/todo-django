from . import abstracts, string_field, color_field, image_field
from enum import Enum

class Field(str, Enum):
    STRING = "string"
    COLOR = "color"
    IMAGE = "image"


field_list: dict[Field, type[abstracts.WidgetList]] = {
    Field.STRING: string_field.MaterializeStringList,
    Field.COLOR: color_field.MaterializeColorList,
    Field.IMAGE: image_field.MaterializeImageList,
}


def get_field_list(field: Field) -> type[abstracts.WidgetList]:
    return field_list[field]