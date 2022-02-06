"""All Urls of To Buy"""

# Libraries
from django.urls import path

# View Todo
from . import views

app_name = 'to_buy'
urlpatterns = [
    path('', views.ToBuyHomeView.as_view(), name='home_buys'),
]

