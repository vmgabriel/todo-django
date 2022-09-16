"""Views of pages"""

# Libraries
from django.views import generic
from django.shortcuts import render


class HomeView(generic.TemplateView):
    """The Main Page"""
    template_name = 'home.html'

    def get(self, request):
        args = {
            "user": self.request.user,
        }
        return render(request, self.template_name, args)
