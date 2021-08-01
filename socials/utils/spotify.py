"""Spotify Connection API"""

import requests
import base64
import six
from typing import Tuple
from django.conf import settings

from ..models import SocialConnection


def _bearer_auth(authorization: str) -> str:
    """Generate bearer auth"""
    return f"Bearer {authorization}"


def _make_authorization_headers(client_id, client_secret):
    """Generate a header content authorization"""
    auth_header = base64.b64encode(
        six.text_type(client_id + ":" + client_secret).encode("ascii")
    )
    return f"Basic {auth_header.decode('ascii')}"


def get_token(code: str) -> Tuple[dict, int]:
    """Generate the token for use"""
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    }
    header = {
        "Authorization": _make_authorization_headers(
            settings.SPOTIFY_CLIENT_ID,
            settings.SPOTIFY_CLIENT_SECRET
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    response = requests.post(url, data=data, headers=header)
    return response.json(), response.status_code


def refresh_token(refresh_token_generated: str) -> dict:
    """Refresh the actual token"""
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_generated
    }
    header = {
        "Authorization": _make_authorization_headers(
            settings.SPOTIFY_CLIENT_ID,
            settings.SPOTIFY_CLIENT_SECRET
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    return requests.post(url, data=data, headers=header).json()


def get_current_user(authorization: str) -> Tuple[dict, int]:
    """Generate the current user"""
    url = "https://api.spotify.com/v1/me"
    response = requests.get(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    return response.json(), response.status_code


def get_user_current_playing_track(authorization: str) -> Tuple[dict, int]:
    """Get The Current Playing track user"""
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    if response.status_code == 204:
        return {"status": "no playing"}, 200
    return response.json(), response.status_code


def change_next_track(authorization: str) -> Tuple[dict, int]:
    """Redirect to next song"""
    url = "https://api.spotify.com/v1/me/player/next"
    response = requests.post(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    if response.status_code == 204:
        return {}, 200
    return response.json(), response.status_code


def change_previous_track(authorization: str) -> Tuple[dict, int]:
    """Redirect to previous song"""
    url = "https://api.spotify.com/v1/me/player/previous"
    response = requests.post(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    if response.status_code == 204:
        return {}, 200
    return response.json(), response.status_code


def start_track(authorization: str) -> Tuple[dict, int]:
    """start the track"""
    url = "https://api.spotify.com/v1/me/player/play"
    response = requests.put(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    if response.status_code == 204:
        return {}, 200
    return response.json(), response.status_code


def pause_track(authorization: str) -> Tuple[dict, int]:
    """pause the track"""
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers={
        "Authorization": _bearer_auth(authorization)
    })
    if response.status_code == 204:
        return {}, 200
    return response.json(), response.status_code


def generate_token(connection: SocialConnection):
    """generate and save token"""
    token_dict, _ = get_token(connection.code)
    connection.refresh_token = token_dict.get("refresh_token")
    connection.access_token = token_dict.get("access_token")
    connection.save()


def regenerate_token(connection: SocialConnection):
    """generate and save token"""
    token_dict = refresh_token(connection.refresh_token)
    connection.access_token = token_dict.get("access_token")
    connection.save()


def generate_content(connection: SocialConnection, func, *args, **kwargs) -> dict:
    """Generate context if not exist"""
    if not connection.access_token:
        generate_token(connection)

    data, status = func(authorization=connection.access_token, *args, **kwargs)
    if status != 200:
        regenerate_token(connection)
        data, status = get_current_user(connection.access_token)

    return data
