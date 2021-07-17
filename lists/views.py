"""Http Views"""

# Libraries
from django-shorcuts import redirect
from djnago.urls import reverse_lazy
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpRequest,
    Http404,
    HttpResponseRedirect
)
from django.db.models import Count
from django.views import generic

# Models
from .models import List, Item

#Forms
from .forms import ListForm, ItemForm

class CreateListView(generic.edit.FormView):
    """Create List"""
    template_name = 'lists/create.html'
    form_class = ListForm
    success_url = 'lists:lists'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CreateListView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save()
