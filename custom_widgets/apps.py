"""Custome Widgets for materialize"""


from django.apps import AppConfig


class CustomWidgetsConfig(AppConfig):
    """Custom Widgets Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_widgets'