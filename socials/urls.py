"""Urls of Socials"""

# Libraries
from django.urls import path

# View Todo
from . import views


app_name = 'social'
urlpatterns = [
    # Auth
    path('spotify/', views.spotify_redirect, name='spotify-redirect'),
    path('spotify/connect', views.spotify_connect, name='spotify-connect'),

    # Profile
    path('spotify/profile', views.spotify_profile, name='spotify-profile'),
]
