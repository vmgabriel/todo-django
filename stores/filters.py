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