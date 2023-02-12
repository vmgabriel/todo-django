"""All tags"""

from django import template
from custom_widgets.list import list_object
from django.template.defaulttags import URLNode
from django.utils.regex_helper import _lazy_re_compile


# Regex for token keyword arguments
kwarg_re = _lazy_re_compile(r"(?:(\w+)=)?(.+)")

register = template.Library()


class UrlCustomFormat(template.Node):
    def __init__(self, parser, url, is_back=False):
        self.parser = parser
        self.url = parser.compile_filter(url)
        self.is_back = is_back

    def render(self, context):
        try:
            obj = context.dicts[-1].get("object")
            fields_in_obj = context.dicts[-2].get("extra", {}).get(
                "fields_in_url" if not self.is_back else "fields_back",
                {}
            )
            kwargs = {name: self.parser.compile_filter(field) for name, field in fields_in_obj.items()}
            return URLNode(self.url, [], kwargs, None).render(context)
        except template.VariableDoesNotExist:
            return ''


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.simple_tag()
def render(obj, widget: list_object.ListComponent, **kwargs):
    return widget.custom_widget.render(widget.to_show, getattr(obj, widget.name))


@register.tag
def url_object_list(parser, token):
    _, url = token.split_contents()
    return UrlCustomFormat(parser, url)

@register.tag
def url_object(parser, token):
    _, url = token.split_contents()
    return UrlCustomFormat(parser, url, is_back=True)
