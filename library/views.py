# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render, redirect
from . import forms


class LibraryView(LoginRequiredMixin, generic.TemplateView):
    """The Main Page"""
    template_name = 'library/index.html'

    def get(self, request):
        args = {
            "user": self.request.user,
        }
        return render(request, self.template_name, args)


class LibraryNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'library/edit.html'
    form_class = forms.BookForm
    success_url = "library:home"
    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(LibraryNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())