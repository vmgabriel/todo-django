import django_filters
from django.db import models
from django.db.models import Model
from django.http import HttpResponse
from django_filters.views import FilterView
from django.template import loader
from django.conf import settings
from . import list_object
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet


class Dummy:
    model = ...


class ListFiltered(FilterView):
    request: object
    identifier: str
    fields: list[list_object.ListComponent]
    filterset_class: type[django_filters.FilterSet]
    model: type[models.Model]
    fields_in_url: dict
    url_edit: str | None
    url_delete: str | None
    url_show: str | None
    title: str

    template_list_name = "list/complex.html"
    page_kwarg = "page"
    paginate_by = settings.PAGINATION_LIMIT
    is_valid = False

    object_list: list
    kwargs: dict
    request: object

    def __init__(self, identifier: str, filter_class: type[django_filters.FilterSet], fields: list[list_object.ListComponent], *args, **kwargs):
        self.identifier = identifier
        self.fields = fields
        self.filterset_class = filter_class
        self.model = getattr(getattr(filter_class, "Meta", Dummy()), "model")
        self.kwargs = {}

        if "url_edit" in kwargs:
            self.url_edit = kwargs["url_edit"]
        if "url_delete" in kwargs:
            self.url_delete = kwargs["url_delete"]
        if "url_show" in kwargs:
            self.url_show = kwargs["url_show"]
        self.fields_in_url = kwargs.get("fields_in_url", {})
        self.title = kwargs.get("title") or f"{self.model.__name__} List"
        self.page_kwarg = f"page_{self.model.__name__}"
        super().__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(enabled=True)
        return queryset

    def set_request(self, request: object):
        self.request = request

    def get_context_data(self, *args, **kwargs):
        self.object_list = self.get_queryset(*args, **kwargs)
        self.kwargs = super().get_context_data(*args, **kwargs)
        return {f"list_{self.identifier}": self}

    @property
    def as_div(self) -> HttpResponse:
        ctx = {
            "title": self.title,
            "fields": self.fields,
            "form": self.filterset_class().form,
            "url_delete": getattr(self, "url_delete", None),
            "url_show": getattr(self, "url_show", None),
            "url_edit": getattr(self, "url_edit", None),
            "paginator": self.kwargs.get("paginator"),
            "page_obj": self.kwargs.get("page_obj"),
            "object_list": self.kwargs.get("object_list"),
            "singular": self.model.__name__,
        }
        return loader.render_to_string(self.template_list_name, ctx, self.request, using=None)


class ListsFiltered:
    lists: dict[str, ListFiltered]
    request: object = ...

    def __init__(self, *args, **kwargs):
        self.lists = {}

    def add(self, to_list: ListFiltered):
        self.lists[to_list.identifier] = to_list

    def get(self, identifier: str) -> ListFiltered | None:
        return self.lists.get(identifier)

    def _adjust_request(self, li: ListFiltered) -> ListFiltered:
        li.set_request(self.request)
        return li

    def set_request(self, request: object):
        self.request = request
        [self._adjust_request(li) for li in self.lists.values()]

    def _get_context(self, li: ListFiltered, *args, **kwargs) -> dict:
        return li.get_context_data(*args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict:
        context = {}
        list_contexts = list(map(lambda l: self._get_context(l, *args, **kwargs), self.lists.values()))
        for ctx in list_contexts:
            context = {**context, **ctx}
        return context


class ListComplexMixin:
    lists_to_show: ListsFiltered

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data_list(self, request: object, *args, **kwargs):
        if not self.lists_to_show:
            raise Exception("List to Show in Mixin is required")

        self.lists_to_show.set_request(request)
        list_ctx = self.lists_to_show.get_context_data(*args, **kwargs)
        context = {**kwargs, **list_ctx}

        return context

