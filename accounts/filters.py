
import django_filters
from . import models

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("first_name", "first_name"),
            ("last_name", "last_name"),
        ),

        field_labels={
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "Username",
            "telephone": "Telephone",
        }
    )

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "username", "telephone"]
