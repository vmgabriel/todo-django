"""All Urls of To Buy"""

# Libraries
from django.urls import path

# View Todo
from . import views

app_name = 'to_buy'
urlpatterns = [
    # Home - List
    path('', views.ToBuyHomeView.as_view(), name='home_buys'),

    # List
    path('new', views.ToBuyNewView.as_view(), name='buys_create'),
    path('<int:pk>', views.DetailToBuyView.as_view(), name="buys_show"),
    path('<int:pk>/delete', views.delete_list_to_but, name='buys_delete'),

    path("<int:pk>/items", views.DetailToBuyView.as_view(), name="buys_add_product"),
    path("<int:pk>/items/<int:pk_item>/new", views.ToBuyNewItemView.as_view(), name="buys_add_item_product"),
    path('<int:pk>/items/<int:pk_item>/edit', views.ToBuyEditItemView.as_view(), name="buys_edit_product"),
    path("<int:pk>/items/<int:pk_item>/delete", views.delete_product_to_list, name="buys_delete_product"),

    path("<int:pk>/telegram-send", views.telegram_send_list, name="buys_send_telegram")
]
