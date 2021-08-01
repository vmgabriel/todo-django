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

    # Reproductor
    path('spotify/reproductor', views.SpotifyReproductorView.as_view(), name='spotify-reproductor'),
    path('spotify/reproductor/next', views.next_song_spotify, name='spotify-reproductor-next'),
    path(
        'spotify/reproductor/previous',
        views.previous_song_spotify,
        name='spotify-reproductor-previous'
    ),
    path(
        'spotify/reproductor/play-pause',
        views.play_pause_song_spotify,
        name='spotify-reproductor-play-pause'
    ),
]
