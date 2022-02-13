"""View Products"""

# Libraries
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.conf import settings

# Modules
from . import models, forms


class ProductListView(LoginRequiredMixin, generic.list.ListView):
    model = models.Product
    paginate_by = settings.PAGINATION_LIMIT
    template_name = 'products/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        return context


class ProductNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'products/edit.html'
    form_class = forms.ProductForm
    success_url = 'products:list'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(ProductNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        self.object.categories.set(form.cleaned_data['categories'])
        return redirect(self.get_success_url())


class ProductEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    template_name = 'products/edit.html'
    success_url = 'products:list'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form, *args, **kwargs):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.categories.set(form.cleaned_data['categories'])
        self.object.save()

        return redirect(
            self.get_success_url()
        )


class CategoryListView(LoginRequiredMixin, generic.list.ListView):
    model = models.Category
    paginate_by = settings.PAGINATION_LIMIT
    context_object_name = 'categories'
    template_name = 'categories/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(CategoryListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()

        return context


class CategoryNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'categories/edit.html'
    form_class = forms.CategoryForm
    success_url = 'products:list_categories'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())


class CategoryEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'categories/edit.html'
    success_url = 'products:list_categories'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
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
