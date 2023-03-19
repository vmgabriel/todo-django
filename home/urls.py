"""All Urls of Home"""

# Libraries
from django.urls import path, re_path
from . import views, autocompletes

app_name: str = "home"
urlpatterns: list[path] = [
    path("", views.HomeListView.as_view(), name="home"),

    # Home
    re_path("homes-autocomplete/$", autocompletes.HomeAutoComplete.as_view(), name="home_autocomplete"),
    path("homes/create", views.HomeNewView.as_view(), name="create_home"),
    path("homes/<int:pk>", views.HomeDetailView.as_view(), name="detail_home"),
    path("homes/<int:pk>/edit", views.HomeUpdateView.as_view(), name="edit_home"),
    path("homes/<int:pk>/delete", views.delete_home, name="delete_home"),

    # Department
    re_path(
        "departments-autocomplete/$",
        autocompletes.DepartmentHomeAutoComplete.as_view(),
        name="departments_autocomplete"
    ),
]
