"""View of socials"""

from django.shortcuts import redirect, render
from django.views import generic
from django.conf import settings

from .models import SocialConnection
from . import SocialIntegration
from .utils.spotify import get_current_user, generate_content


def spotify_redirect(request):
    """Send spotify connect url"""
    scope = "user-read-private user-read-email"

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

    current_user = generate_content(social_connect, get_current_user)

    ctx = {
        "current_user": current_user,
        "image": current_user.get('images')[0].get('url'),
    }

    return render(request, "spotify/profile.html", ctx)
