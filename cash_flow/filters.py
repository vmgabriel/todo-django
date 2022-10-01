"""All Filters In Cash Flow"""

# Libraries
import django_filters

# Modules
from . import models


class CategoryFlowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.CategoryFlow
        fields = ["name", "type_flow", "state_flow"]

