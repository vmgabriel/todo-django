"""View Products"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.conf import settings
from custom_widgets.list import basic as list_basic, list_object
from custom_widgets import fields

# Modules
from . import models, forms, filters


class ProductListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = models.Product
    paginate_by = settings.PAGINATION_LIMIT
    template_name = "products/index.html"
    filterset_class = filters.ProductFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "products:new_product"
    url_delete = "products:delete_product"
    url_edit = "products:edit_product"
    title_form = "Products"
    fields_to_show: list[list_object.ListComponent] = [
        list_object.ListComponent(
            "image",
            "",
            fields.Field.IMAGE,
        ),
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
            "categories",
            "Categories",
            fields.Field.CHIP,
        ),
    ]


class ProductNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = "products/edit.html"
    form_class = forms.ProductForm
    success_url = "product.list"
    form_name = "Product"
    fields_in_url = {}
    url_cancel = "products:list"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(ProductNewView, self).get_context_data(**kwargs)
        context["mode"] = "Save"
        context["form_name"] = self.form_name
        context["fields_in_url"] = self.fields_in_url
        context["url_cancel"] = self.url_cancel
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            user=self.request.user,
        )
        self.object.save()
        self.object.categories.set(form.cleaned_data["categories"])
        return redirect(self.get_success_url())


class ProductEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    template_name = 'products/edit.html'
    success_url = 'products:list'
    form_name = "Product"
    fields_in_url = {}
    url_cancel = "products:list"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context["mode"] = "Update"
        context["form_name"] = self.form_name
        context["fields_in_url"] = self.fields_in_url
        context["url_cancel"] = self.url_cancel
        return context

    def form_valid(self, form, *args, **kwargs):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.categories.set(form.cleaned_data['categories'])
        self.object.save()

        return redirect(
            self.get_success_url()
        )

class CategoryListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = models.Category
    paginate_by = settings.PAGINATION_LIMIT
    template_name = 'categories/index.html'
    filterset_class = filters.CategoryFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "products:new_category"
    url_delete = "products:delete_category"
    url_edit = "products:edit_category"
    title_form = "Categories"
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
            "color",
            "Color",
            fields.Field.COLOR,
        ),
    ]

class CategoryNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = "categories/edit.html"
    form_class = forms.CategoryForm
    success_url = "products:list_categories"
    form_name = "Product Category"
    fields_in_url = {}
    url_cancel = "products:list_categories"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryNewView, self).get_context_data(**kwargs)
        context["mode"] = "Save"
        context["form_name"] = self.form_name
        context["fields_in_url"] = self.fields_in_url
        context["url_cancel"] = self.url_cancel
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            user=self.request.user,
        )
        self.object.save()
        return redirect(self.get_success_url())


class CategoryEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = "categories/edit.html"
    success_url = "products:list_categories"
    form_name = "Product Category"
    fields_in_url = {}
    url_cancel = "products:list_categories"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryEditView, self).get_context_data(**kwargs)
        context["mode"] = "Update"
        context["form_name"] = self.form_name
        context["fields_in_url"] = self.fields_in_url
        context["url_cancel"] = self.url_cancel
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.save()
        return redirect(
            self.get_success_url()
        )


@login_required
def delete_category(request, pk):
    model = models.Category
    category = get_object_or_404(model, pk=pk)
    category.enabled = False
    category.save()
    return redirect("products:list_categories")


@login_required
def delete_product(request, pk):
    model = models.Product
    product = get_object_or_404(model, pk=pk)
    product.enabled = False
    product.save()
    return redirect("products:list")
