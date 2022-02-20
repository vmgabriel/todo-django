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
    path("<int:pk>/delete", views.delete_store, name="delete"),
    path("<int:pk>", views.DetailStoreView.as_view(), name="detail"),
    path("<int:pk>/products/new", views.add_product_to_store, name="add_product"),
    path("<int:pk>/products/<int:pk_item>/edit", views.edit_product_to_store, name="edit_product"),
    path("<int:pk>/products/<int:pk_item>/delete", views.delete_product_to_store, name="delete_product"),
]
