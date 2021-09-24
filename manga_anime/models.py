"""Manga Anime Models"""

# Libraries
from django.db import models

# Modules
from manga_anime import TypeFavorite


class FavoriteMangaAnime(models.Model):
    title = models.CharField("Title", max_length=70)
    description = models.TextField("Description", blank=True, null=True)
    type = models.CharField("Type", max_length=10, choices=TypeFavorite.CHOICES, default=TypeFavorite.ANIME)
    uid_anime = models.PositiveIntegerField("Id Anime")
    url_anime = models.CharField("Url Anime", max_length=70)
    url_image = models.CharField("Url Image", max_length=90)
