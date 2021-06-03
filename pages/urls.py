"""Url Pages"""

# Libraries
from django.urls import path

# View Todo
from . import views


app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
