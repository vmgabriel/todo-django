from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, get_object_or_404

from custom_widgets.list import basic as list_basic, list_object
from custom_widgets import fields
from custom_widgets.list.several import ListsFiltered, ListFiltered, ListComplexMixin
from . import models, filters, forms, enums


def save_history_home(request, history: models.HomeHistory):
    history.created_by = request.user
    history.updated_by = request.user
    history.save()


class HomeListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    template_name = "home/home.html"
    model = models.Home
    paginate_by = settings.PAGINATION_LIMIT
    filterset_class = filters.HomeFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "home:create_home"
    url_edit = "home:edit_home"
    url_delete = "home:delete_home"
    url_view = "home:detail_home"
    title_form = "Homes"
    fields_to_show: list[list_object.ListComponent] = [
        list_object.ListComponent(
            "name",
            "Name",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "description",
            "Description",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "direction",
            "Direction",
            fields.Field.STRING,
        ),
    ]


class HomeNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = "home/edit.html"
    form_class = forms.HomeForm
    success_url = "home:home"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(HomeNewView, self).get_context_data(**kwargs)
        context["mode"] = "Save"
        context["form_name"] = "Home"
        context["fields_in_url"] = {}
        context["url_cancel"] = "home:home"
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user}
        )
        self.object.save()
        save_history_home(self.request, models.HomeHistory(
            home=self.object.pk,
            note=f"Home Created",
            state=enums.HomeState.INFO,
        ))
        return redirect(self.get_success_url())


class HomeUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    """Update Home view."""
    template_name = "home/edit.html"
    success_url = reverse_lazy('home:home')
    form_class = forms.HomeForm
    model = models.Home

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "Edit"
        context["form_name"] = "Home"
        context["fields_in_url"] = {}
        context["url_cancel"] = "home:home"
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True, user=self.request.user)
        self.object.administrators.set(form.cleaned_data["administrators"])
        self.object.save()
        return redirect(
            self.get_success_url()
        )


class HomeDetailView(LoginRequiredMixin, ListComplexMixin, generic.detail.DetailView):
    """Home Details View"""
    template_name = "home/index.html"
    model = models.Home
    paginate_by = settings.PAGINATION_LIMIT
    lists_to_show: ListsFiltered

    def __init__(self, *args, **kwargs):
        self.lists_to_show = ListsFiltered(*args, **kwargs)
        self.lists_to_show.add(
            ListFiltered(
                "history",
                filters.HomeHistoryFilter, [
                    list_object.ListComponent(
                        "home.name",
                        "Home",
                        fields.Field.STRING,
                    ),
                    list_object.ListComponent(
                        "note",
                        "Note",
                        fields.Field.STRING,
                    ),
                    list_object.ListComponent(
                        "state",
                        "State",
                        fields.Field.STRING,
                    ),
                ],
            ),
        )
        self.lists_to_show.add(
            ListFiltered(
                "floor",
                filters.HomeFloorFilter,
                [
                    list_object.ListComponent(
                        "number",
                        "Number",
                        fields.Field.STRING,
                    ),
                ],
                url_create="home:new_floor",
                url_delete="home:delete_floor",
                url_edit="home:edit_floor",
                fields_in_url={"pk": "object.id"}
            ),
        )
        self.lists_to_show.add(
            ListFiltered("department", filters.HomeDepartmentFilter, [
                list_object.ListComponent(
                    "code",
                    "Code",
                    fields.Field.STRING,
                ),
                list_object.ListComponent(
                    "home.name",
                    "Home",
                    fields.Field.STRING,
                ),
            ]),
        )
        self.lists_to_show.add(
            ListFiltered("group", filters.DepartmentGroupHome, [
                list_object.ListComponent(
                    "code",
                    "Code",
                    fields.Field.STRING,
                ),
                list_object.ListComponent(
                    "home.name",
                    "Home",
                    fields.Field.STRING,
                ),
            ]),
        )
        super().__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data_list(request=self.request, *args, **context)
        return context


class FloorNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = "floor/edit.html"
    form_class = forms.FloorForm
    success_url = "home:home"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super().get_context_data(**kwargs)
        context["mode"] = "Save"
        context["form_name"] = "Floor"
        context["fields_in_url"] = {}
        context["url_cancel"] = "home:home"
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())


class FloorUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    """Floor Update Home view."""
    template_name = "floor/edit.html"
    success_url = reverse_lazy("home:home")
    form_class = forms.FloorForm
    model = models.FloorHome

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "Edit"
        context["form_name"] = "Floor"
        context["fields_in_url"] = {}
        context["url_cancel"] = "home:home"
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True, user=self.request.user)
        self.object.save()
        save_history_home(self.request, models.HomeHistory(
            home=self.object.home,
            note=f"Floor {self.object.number} Updated",
            state=enums.HomeState.INFO,
        ))
        return redirect(self.get_success_url())


@login_required
def delete_home(request, pk):
    model = models.Home
    instance = get_object_or_404(model, pk=pk)
    instance.enabled = False
    save_history_home(request, models.HomeHistory(
        home=instance.home,
        note="Home Deleted",
        state=enums.HomeState.INFO,
    ))
    instance.save()
    return redirect("home:home")


@login_required
def delete_floor(request, pk):
    model = models.FloorHome
    instance = get_object_or_404(model, pk=pk)
    instance.enabled = False
    save_history_home(request, models.HomeHistory(
        home=instance.home,
        note=f"Floor {instance.number} Deleted",
        state=enums.HomeState.INFO,
    ))
    instance.save()
    return redirect("home:home")
