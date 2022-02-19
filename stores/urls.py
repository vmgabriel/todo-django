"""Url Store"""
# Libraries
from django.urls import path

# View Todo
from . import views

app_name = 'stores'
urlpatterns = [
    path('', views.StoreListView.as_view(), name="list"),
    path('create', views.StoreNewView.as_view(), name="create"),
    path('<int:pk>/edit', views.StoreEditView.as_view(), name="update"),
    path("<int:pk>/delete", views.delete_store, name="delete")
]
