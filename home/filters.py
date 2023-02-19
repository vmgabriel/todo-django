"""Home Filters"""

import django_filters
from . import models
from accounts import models as account_models
from custom_widgets.multiple_autocomplete_select_list.multiple_autocomplete_select import MaterializeModelSelect2Multiple


class HomeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    direction = django_filters.CharFilter(lookup_expr="icontains")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("direction", "direction"),
        ),

        field_labels={
            "name": "Name",
            "direction": "Address",
        }
    )

    class Meta:
        model = models.Home
        fields = ["name", "direction"]


class HomeFloorFilter(django_filters.FilterSet):
    number = django_filters.NumberFilter()
    ordering = django_filters.OrderingFilter(
        fields=(
            ("number", "number"),
        ),

        field_labels={
            "number": "number",
        }
    )

    class Meta:
        model = models.FloorHome
        fields = ["number"]


class HomeHistoryFilter(django_filters.FilterSet):
    home = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Home.objects.all(),
        conjoined=True,
        widget=MaterializeModelSelect2Multiple(url="home:home_autocomplete"),
    )
    updated_at = django_filters.DateTimeFromToRangeFilter()
    ordering = django_filters.OrderingFilter(
        fields=(
            ("home", "home"),
            ("updated_at", "updated_at"),
        ),

        field_labels={
            "home": "Home",
            "updated_at": "Updated At",
        }
    )

    class Meta:
        model = models.HomeHistory
        fields = ["home", "state", "updated_at"]


class HomeDepartmentFilter(django_filters.FilterSet):
    home = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Home.objects.all(),
        conjoined=True,
        widget=MaterializeModelSelect2Multiple(url="home:home_autocomplete"),
    )
    code = django_filters.CharFilter(lookup_expr="icontains")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("home", "home"),
            ("code", "code"),
        ),

        field_labels={
            "home": "Home",
            "code": "Code",
        }
    )

    class Meta:
        model = models.DepartmentHome
        fields = ["home", "code"]


class DepartmentGroupHome(django_filters.FilterSet):
    is_responsible = django_filters.BooleanFilter()
    department = django_filters.ModelMultipleChoiceFilter(
        queryset=models.DepartmentHome.objects.all(),
        conjoined=True,
        widget=MaterializeModelSelect2Multiple(url="home:departments_autocomplete"),
    )
    user = django_filters.ModelMultipleChoiceFilter(
        queryset=account_models.User.objects.all(),
        conjoined=True,
        widget=MaterializeModelSelect2Multiple(url="accounts:user_autocomplete"),
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("department", "department"),
            ("user", "user"),
            ("is_responsible", "is_responsible"),
        ),

        field_labels={
            "department": "Department",
            "user": "User",
            "is_responsible": "Is Responsible",
        }
    )

    class Meta:
        model = models.DepartmentGroupHome
        fields = ["department", "user", "is_responsible"]
