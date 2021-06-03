"""Views of pages"""

# Libraries
from django.views import generic


class HomeView(generic.TemplateView):
    """The Main Page"""
    template_name = 'home.html'
