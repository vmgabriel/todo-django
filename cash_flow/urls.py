"""All Flows"""

# Libraries
from django.urls import path
from . import views

app_name: str = "cash_flow"
urlpatterns: list[path] = [
    path("", views.CashFlowHomeView.as_view(), name='home_cash_flow'),

    # Money Flow
    path("money/new", views.FlowMoneyNewView.as_view(), name="money"),
    path("money/edit/<int:pk>", views.FlowMoneyEditView.as_view(), name="money_edit"),

    # Categories
    path("categories", views.CategoryFlowListView.as_view(), name="categories"),
    path("categories/new", views.CategoryFlowNewView.as_view(), name="new_category"),
    path("categories/edit/<int:pk>", views.CategoryFlowEditView.as_view(), name="edit_category"),
    path("categories/delete/<int:pk>", views.delete_category, name="delete_category"),
]