"""All Filters In Products"""

# Libraries
from django import forms
from dal import autocomplete
import django_filters

# Modules
from . import models
from custom_widgets.multiple_autocomplete_select_list.multiple_autocomplete_select import MaterializeModelSelect2Multiple
from custom_widgets.multiple_select_list.multiple_select_materialize import MaterializeCheckboxSelectMultiple

class BooksFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    genres = django_filters.ModelMultipleChoiceFilter(
        # field_name='book_genres',
        queryset=models.BookGenres.objects.all(),
        conjoined=True,
        widget=MaterializeCheckboxSelectMultiple(),
    )
    authors = django_filters.ModelMultipleChoiceFilter(
        # field_name='authors',
        queryset=models.Authors.objects.all(),
        conjoined=True,
        widget=MaterializeModelSelect2Multiple(url="library:author-autocomplete"),
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
