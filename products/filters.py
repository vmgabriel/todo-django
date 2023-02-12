"""All Filters In Products"""

# Libraries
from django import forms
import django_filters

# Modules
from . import models


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    categories = django_filters.ModelMultipleChoiceFilter(
        # field_name='categories',
        queryset=models.Category.objects.all(),
        conjoined=True,
        widget=forms.CheckboxSelectMultiple(),
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),

        field_labels={
            'name': 'Name Product',
        }
    )

    class Meta:
        model = models.Product
        fields = ["name", "categories"]

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),

        field_labels={
            'name': 'Category Name',
        }
    )

    class Meta:
        model = models.Category
        fields = ["name"]