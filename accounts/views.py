"""Created Views of Accounts Application"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Forms
from .forms import UserForm

# Models
from .models import User


class SignUpView(generic.CreateView):
    """Create View Sign Up of account"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UpdateProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    """Update profile view."""
    template_name = 'profiles/edit.html'
    form_class = UserForm
    model = User

    def get_object(self):
        """Return user"""
        return self.request.user
