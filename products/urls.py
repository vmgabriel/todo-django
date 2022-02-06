"""All URL Products"""

# Libraries
from django.urls import path

# View Todo
from . import views

app_name = 'products'
urlpatterns = [
    # Products
    path('', views.ProductListView.as_view(), name='list'),
    path('new', views.ProductNewView.as_view(), name='new_product'),
    path('<int:pk>/edit', views.ProductEditView.as_view(), name='edit_product'),
    path('<int:pk>/delete', views.delete_product, name='delete_product'),

    # Categories
    path('categories', views.CategoryListView.as_view(), name='list_categories'),
    path('categories/new', views.CategoryNewView.as_view(), name='new_category'),
    path('categories/<int:pk>/edit', views.CategoryEditView.as_view(), name='edit_category'),
    path('categories/<int:pk>/delete', views.delete_category, name='delete_category'),
]
