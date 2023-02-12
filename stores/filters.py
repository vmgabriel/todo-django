import django_filters
from . import models, forms

class StoreProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        name="product__name",
        lookup_expr="icontains",
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
        ),

        field_labels={
            'name': 'Name Product',
        }
    )

    class Meta:
        model = models.StoreProduct
        fields = ["name"]


class StoreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
    )
    description = django_filters.CharFilter(
        lookup_expr="icontains",
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("description", "description"),
        ),

        field_labels={
            'name': 'Name Store',
            'description': 'Description Store',
        }
    )

    class Meta:
        model = models.Store
        fields = ["name", "description"]
