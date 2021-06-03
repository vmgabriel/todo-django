"""App Config Base"""

# Libraries
from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Pages Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
