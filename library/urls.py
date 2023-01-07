"""Url Pages"""

# Libraries
from django.urls import path

# Views
from . import views


app_name = 'library'
urlpatterns = [
    path('', views.LibraryView.as_view(), name='home'),
]
