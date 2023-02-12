from django.db.models import Model
from django.http import HttpResponse
from django_filters.views import FilterView
from django.template import loader
from django.conf import settings
from . import list_object


class ListSet:
    def __init__(
            self,
            request,
            template_list_name: str,
            title_form: str,
            fields_to_show: list[list_object.ListComponent],
            create_url,
            **kwargs
    ):
        self.create_url = create_url
        self.request = request
        self.template_list_name = template_list_name
        self.title_form = title_form
        self.kwargs = kwargs
        self.fields_to_show = fields_to_show

    @property
    def as_div(self) -> HttpResponse:
        ctx = {
            "created_url": self.create_url,
            "title_form": self.title_form,
            "fields_to_show": self.fields_to_show,
            "extra": self.kwargs,
        }
        return loader.render_to_string(self.template_list_name, ctx, self.request, using=None)



class ListBasicMixin(FilterView):
    model: Model
    url_create: str
    url_delete: str
    url_edit: str
    url_view: str
    title_form: str
    fields_to_show: list[list_object.ListComponent]
    fields_in_url: dict
    fields_back: dict

    paginate_by = settings.PAGINATION_LIMIT
    template_list_name = "list/basic.html"


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["list_view"] = ListSet(
            request=self.request,
            template_list_name=self.template_list_name,
            create_url=getattr(self, "url_create", None),
            title_form=self.title_form,
            fields_to_show=self.fields_to_show or [],
            fields_in_url=self.fields_in_url or {},
            fields_back= self.fields_back or {},
            url_delete=getattr(self, "url_delete", None),
            url_edit=getattr(self, "url_edit", None),
            url_view=getattr(self, "url_view", None),
            **context
        )
        return context