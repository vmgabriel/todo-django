"""Created Views of Accounts Application"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

# Forms
from .forms import UserForm, RegisterForm, UserFormAdmin

# Models
from .models import User
from socials.models import SocialConnection


class SignUpView(LoginRequiredMixin, generic.edit.FormView):
    """Create View Sign Up of account"""
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        self.object = form.save(
            commit=False
        )
        self.object.save()
        return redirect(self.get_success_url())


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


class UserListView(LoginRequiredMixin, generic.list.ListView):
    model = User
    paginate_by = settings.PAGINATION_LIMIT
    template_name = 'users/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        return context


class CreateAdminView(LoginRequiredMixin, generic.edit.FormView):
    """Create View Sign Up of account"""
    form_class = UserFormAdmin
    success_url = reverse_lazy('accounts:users')
    template_name = 'users/edit.html'

    def form_valid(self, form):
        self.object = form.save(
            commit=False
        )
        self.object.is_staff = self.object.is_superuser
        self.object.save()
        return redirect(self.get_success_url())


@login_required
def delete_user(request, pk):
    model = User
    user = get_object_or_404(model, pk=pk)
    user.is_active = False
    user.save()
    return redirect("accounts:users")
