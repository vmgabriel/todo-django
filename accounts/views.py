"""Created Views of Accounts Application"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from custom_widgets.list import basic as list_basic, list_object
from custom_widgets import fields
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

# Forms
from .forms import UserForm, RegisterForm, UserFormAdmin
from . import filters

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


class UserListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = User
    paginate_by = settings.PAGINATION_LIMIT
    template_name = "users/index.html"
    filterset_class = filters.UserFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "accounts:create_user"
    url_delete = "accounts:delete_user"
    title_form = "Users"
    fields_to_show: list[list_object.ListComponent] = [
        list_object.ListComponent(
            "image",
            "",
            fields.Field.IMAGE,
        ),
        list_object.ListComponent(
            "username",
            "Username",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "first_name",
            "First Name",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "last_name",
            "Last Name",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "telephone",
            "Phone",
            fields.Field.STRING,
        ),
    ]

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
        self.object.set_password(self.object.password)
        self.object.save()
        return redirect(self.get_success_url())


@login_required
def delete_user(request, pk):
    model = User
    user = get_object_or_404(model, pk=pk)
    user.is_active = False
    user.save()
    return redirect("accounts:users")
