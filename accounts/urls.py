"""Accounts Session of User"""

# Libraries
from django.urls import path

# Views
from . import views


app_name = 'accounts'
urlpatterns = [
    path(
        'signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),

    path(
        'me/profile/',
        views.UpdateProfileView.as_view(),
        name='profile-user',
    ),

    path(
        '',
        views.UserListView.as_view(),
        name='users',
    ),
    path('<int:pk>/delete', views.delete_user, name='delete_user'),
    path("create", views.CreateAdminView.as_view(), name="create_user"),
]
