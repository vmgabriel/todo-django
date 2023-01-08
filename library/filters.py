"""All Filters In Products"""

# Libraries
from django import forms
import django_filters

# Modules
from . import models

class BooksFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    genres = django_filters.ModelMultipleChoiceFilter(
        # field_name='book_genres',
        queryset=models.BookGenres.objects.all(),
        conjoined=True,
        widget=forms.CheckboxSelectMultiple(),
    )
    authors = django_filters.ModelMultipleChoiceFilter(
        # field_name='authors',
        queryset=models.Authors.objects.all(),
        conjoined=True,
        widget=forms.CheckboxSelectMultiple(),
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),

        field_labels={
            'name': 'Name Book',
        }
    )

    class Meta:
        model = models.Books
        fields = ["name", "genres", "authors"]

class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),

        field_labels={
            'name': 'Name Author',
        }
    )

    class Meta:
        model = models.Authors
        fields = ["name"]
