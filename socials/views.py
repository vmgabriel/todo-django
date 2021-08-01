"""View of socials"""

import json
from django.shortcuts import redirect, render
from django.views import generic
from django.conf import settings

from .models import SocialConnection
from . import SocialIntegration
from .utils import spotify


def spotify_redirect(request):
    """Send spotify connect url"""
    scope = "user-modify-playback-state"

    auth_url = "https://accounts.spotify.com/authorize"
    auth_url += "?response_type=code"
    auth_url += f"&client_id={settings.SPOTIFY_CLIENT_ID}"
    auth_url += f"&scope={scope}"
    auth_url += f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
    return redirect(auth_url)


def spotify_connect(request):
    """Connect and save data"""
    code = request.GET["code"]

    if request.GET["code"]:
        social_connection = SocialConnection.objects.get(
            social_connect=SocialIntegration.SPOTIFY,
            user=request.user
        )
        if social_connection:
            social_connection.code = code
        else:
            social_connection = SocialConnection(code=code, user=request.user)
        social_connection.save()

    return redirect("accounts:profile-user")


def spotify_profile(request):
    """Get Info of spotify profile"""
    social_connect = SocialConnection.objects.get(user=request.user)

    current_user = spotify.generate_content(social_connect, spotify.get_current_user)

    ctx = {
        "current_user": current_user,
        "image": current_user.get('images')[0].get('url'),
    }

    return render(request, "spotify/profile.html", ctx)


class SpotifyReproductorView(generic.TemplateView):
    """The Main Page"""
    template_name = 'spotify/reproductor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_connect = SocialConnection.objects.filter(user=self.request.user)

        if not social_connect or not social_connect.code:
            return redirect("socials:spotify-redirect")

        social_connect = social_connect.first()

        playing_track = spotify.generate_content(social_connect, spotify.get_user_current_playing_track)

        if "status" in playing_track and playing_track.get("status") == "no_playing":
            context['has_playing'] = False
        else:
            context['has_playing'] = True
            context['spotify-track'] = playing_track
            context['image_album'] = playing_track.get("item").get("album").get("images")[0].get("url")
            context['artists'] = playing_track.get("item").get("album").get("artists")
            context['name_song'] = playing_track.get("item").get("name")
        return context


def next_song_spotify(request):
    """to next song"""
    social_connect = SocialConnection.objects.get(user=request.user)
    spotify.generate_content(social_connect, spotify.change_next_track)
    return redirect("social:spotify-reproductor")


def previous_song_spotify(request):
    """to previous song"""
    social_connect = SocialConnection.objects.get(user=request.user)
    spotify.generate_content(social_connect, spotify.change_previous_track)
    return redirect("social:spotify-reproductor")


def play_pause_song_spotify(request):
    """Play or Pause Song"""
    social_connect = SocialConnection.objects.get(user=request.user)
    has_paused = True
    function = spotify.start_track if has_paused else spotify.pause_track
    spotify.generate_content(social_connect, function)
    return redirect("social:spotify-reproductor")
