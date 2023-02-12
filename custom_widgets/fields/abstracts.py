from django.utils.safestring import mark_safe
from django.forms import renderers


class WidgetList:
    template_name: str

    def _render(self, template_name, context, renderer=None):
        if renderer is None:
            renderer = renderers.get_default_renderer()
        return mark_safe(renderer.render(template_name, context))

    def render(self, name, value, attrs: dict=None, renderer=None):
        attrs = attrs or {}
        attrs["name"] = name
        attrs["value"] = value
        return self._render(self.template_name, attrs, renderer)