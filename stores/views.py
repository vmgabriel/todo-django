"""Store Views"""

# Libraries
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.conf import settings
from django.db.models import Q, QuerySet
from django.core.paginator import Paginator
from djmoney.money import Money
from custom_widgets.list import basic as list_basic, list_object
from custom_widgets import fields

# Modules
from . import models, forms, filters
from products import models as product_models


class StoreListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = models.Store
    paginate_by = settings.PAGINATION_LIMIT
    template_name = "stores/index.html"
    filterset_class = filters.StoreFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "stores:create"
    url_view = "stores:detail"
    url_edit = "stores:update"
    url_delete = "stores:delete"
    title_form = "Stores"
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
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = super(StoreListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(StoreListView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        return context


class StoreNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'stores/edit.html'
    form_class = forms.StoreForm
    success_url = 'stores:list'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        # context = super(StoreNewView, self).get_context_data(**kwargs)
        context = {}
        context['mode'] = 'Save'
        context['form'] = self.form_class(self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())


class StoreEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = 'stores/edit.html'
    success_url = 'stores:list'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(StoreEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form, *args, **kwargs):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()

        return redirect(
            self.get_success_url()
        )


class DetailStoreView(LoginRequiredMixin, generic.detail.DetailView):
    """Detail Board View"""
    model = models.Store
    template_name = 'stores/detail.html'

    def queryset_list(self, pk):
        return models.StoreProduct.objects.filter(enabled=True, store=pk)

    def queryset_products(self, pk, query = None):
        my_list = [x.product.pk for x in self.queryset_list(pk)]
        data = (
            product_models.Product.objects.filter(
                enabled=True,
            )
            .exclude(pk__in=my_list)
        )
        if query:
            data = data.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return data

    def filter_query(
            self,
            query: QuerySet,
            filters: dict,
            prefix: str = "to_include_",
            is_included: bool = False,
    ) -> QuerySet:
        base_filter: dict = {
            key[len(prefix):]: value
            for key, value in filters.items()
            if key.startswith(prefix)
        }
        for key, value in base_filter.items():
            field = ""
            if key == "name":
                if is_included:
                    field = "product__"
                field += "name__icontains"
            if key == "categories" and value != "":
                value = [int(pk) for pk in value.split(",")]
                if is_included:
                    field = "product__"
                field += "categories__in"
            query = query.filter(Q(**{field: value}))
        return query

    def paginate(self, data: QuerySet) -> Paginator:
        return Paginator(data, settings.PAGINATION_LIMIT)

    def get_categories(self) -> dict:
        categories = product_models.Category.objects.filter(enabled=True)
        return {category.name: category.id for category in categories}

    def get_context_data(self, *args, **kwargs):
        """Context generated by detail board"""
        context = super().get_context_data(**kwargs)
        query: dict = {key: value for key, value in self.request.GET.dict().items() if key != ""} or {}

        products = self.paginate(self.filter_query(self.queryset_products(
            context["store"]
        ), query))
        count_products = products.count
        products = products.page(self.request.GET.get("page_products", 1))

        items = self.paginate(self.filter_query(
            self.queryset_list(context['store']),
            query,
            "included_",
            True,
        ))
        count_items = items.count
        items = items.page(self.request.GET.get("page_items", 1))

        context['items'] = items
        context['products'] = products
        context["count_products"] = count_products
        context["form_item"] = forms.StoreProductForm(context['store'])
        context["count_items"] = count_items
        context["search"] = query.get("to_include_name", "")
        context["search_included"] = query.get("included_name", "")
        context["selected_categories"] = [
            int(x)
            for x in query.get("to_include_categories", "").split(",")
            if x != ""
        ]
        context["selected_categories_included"] = [
            int(x)
            for x in query.get("included_categories", "").split(",")
            if x != ""
        ]
        context["categories"] = self.get_categories()
        return context


@login_required
def delete_store(request, pk):
    model = models.Store
    store = get_object_or_404(model, pk=pk)
    store.enabled = False
    store.save()
    return redirect("stores:list")


@login_required
def add_product_to_store(request, pk):
    model_history = models.StoreProductHistory
    form = forms.StoreProductCompleteForm(request.POST)
    if form.is_valid:
        object = form.save(
            commit=False,
            user=request.user,
        )
        object.save()
        item_history = model_history(
            store_product=object,
            price=object.price,
            created_by=request.user,
            updated_by=request.user,
        )
        item_history.save()
    return redirect("stores:detail", pk=pk)


@login_required
def edit_product_to_store(request, pk, pk_item):
    model = models.StoreProduct
    model_history = models.StoreProductHistory
    item = get_object_or_404(model, pk=pk_item)
    item.description = request.POST.get("description")
    item.price = Money(request.POST.get("price_0"), request.POST.get("price_1"))
    item_history = model_history(
        store_product=item,
        price=item.price,
        created_by=request.user,
        updated_by=request.user,
    )
    item.save()
    item_history.save()
    return redirect("stores:detail", pk=pk)


@login_required
def delete_product_to_store(request, pk, pk_item):
    model = models.StoreProduct
    item = get_object_or_404(model, pk=pk_item)
    item.enabled = False
    item.save()
    return redirect("stores:detail", pk=pk)
