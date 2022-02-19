"""Sotre Views"""

# Libraries
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.conf import settings
from django_admin_geomap import geomap_context

# Modules
from . import models, forms


class StoreListView(LoginRequiredMixin, generic.list.ListView):
    model = models.Store
    paginate_by = settings.PAGINATION_LIMIT
    template_name = 'stores/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(StoreListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(StoreListView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        context = {**context, **geomap_context(self.get_queryset().all())}
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
        self.object.save()

        return redirect(
            self.get_success_url()
        )

@login_required
def delete_store(request, pk):
    model = models.Store
    store = get_object_or_404(model, pk=pk)
    store.enabled = False
    store.save()
    return redirect("stores:list")
