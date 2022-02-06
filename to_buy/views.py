"""Django Views"""

# Libraries
from django.shortcuts import render
from django.views import generic


class ToBuyHomeView(generic.TemplateView):
    """The Main for to buy Page"""
    template_name = 'to_buy_home.html'

    def get(self, request):
        print("Get to Buy Home")
        args = {"a": 1}
        return render(request, self.template_name, args)
