# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render

class LibraryView(LoginRequiredMixin, generic.TemplateView):
    """The Main Page"""
    template_name = 'library/index.html'

    def get(self, request):
        args = {
            "user": self.request.user,
        }
        return render(request, self.template_name, args)