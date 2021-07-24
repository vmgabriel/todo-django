"""List URLs"""

# Libraries
from django.urls import path

# List Views
from .views import list as list_views

app_name = 'lists'
urlpatterns = [
    path(
        '',
        list_views.ListsListView.as_view(),
        name='lists'
    ),
    path(
        'new/',
        list_views.CreateListView.as_view(),
        name='lists_new'
    )
]
