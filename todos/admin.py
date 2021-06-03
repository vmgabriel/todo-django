"""Admin Configuration"""

# Libraries
from django.contrib import admin

# Modules
from .models import Board, Card


admin.site.register(Board)
admin.site.register(Card)
