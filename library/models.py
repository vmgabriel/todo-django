"""Library Models"""

# Libraries
from django.db import models
from django.utils.translation import gettext_lazy
from versatileimagefield.fields import VersatileImageField
from colorfield.fields import ColorField


class ProgressConversion(models.TextChoices):
    NOT_EXECUTED = "ne", gettext_lazy("No Executed")
    IN_PROGRESS = "p", gettext_lazy("In Progress")
    SUCCESS = "s", gettext_lazy("Success")
    FAIL = "f", gettext_lazy("Fail")

class BookGenres(models.Model):
    """Genres of Books"""
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    color = ColorField()
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.name)

class Authors(models.Model):
    """Authors of Books"""
    name = models.CharField(max_length=60)
    image = VersatileImageField(
        upload_to=f"images/library/authors",
        blank=True,
        null=True,
    )
    description = models.CharField(max_length=120)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.name)

class Books(models.Model):
    name = models.CharField(max_length=150)
    image = VersatileImageField(
        upload_to=f"images/library/books",
        blank=True,
        null=True,
    )

    authors = models.ManyToManyField(Authors, blank=True, null=True)
    
    file = models.FileField(upload_to=f"books", null=False, blank=False)
    file_epub = models.FileField(upload_to=f"books", null=True, blank=True)
    file_mobi = models.FileField(upload_to=f"books", null=True, blank=True)
    progress_conversion = models.CharField(
        max_length=3,
        choices=ProgressConversion.choices,
        default=ProgressConversion.NOT_EXECUTED,
        blank=True,
        null=True
    )
    published_on = models.DateTimeField(blank=True, null=True)
    raiting = models.PositiveIntegerField(default=0)
    
    genres = models.ManyToManyField(BookGenres, blank=True, null=True)
    
    description = models.CharField(max_length=250, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Book - name: {}".format(self.name)

