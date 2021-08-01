"""Created Views of Accounts Application"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

# Forms
from .forms import UserForm, RegisterForm

# Models
from .models import User
from socials.models import SocialConnection


class SignUpView(generic.CreateView):
    """Create View Sign Up of account"""
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UpdateProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    """Update profile view."""
    template_name = 'profiles/edit.html'
    success_url = reverse_lazy('accounts:profile-user')
    form_class = UserForm
    model = User

    def get_object(self):
        """Return user"""
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_spotify_connection'] = SocialConnection.objects.filter(
            user=context.get('user')
        ).exists()
        return context
