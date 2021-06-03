"""Created Views of Accounts Application"""

# Libraries
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    """Create View Sign Up of account"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
