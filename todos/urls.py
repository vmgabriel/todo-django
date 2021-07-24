
"""Url todos"""

# Libraries
from django.urls import path

# View Todo
from . import views


app_name = 'todos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'boards/',
        views.ListBoardView.as_view(),
        name='boards'
    ),
    path(
        'boards/new/',
        views.CreateBoardView.as_view(),
        name='boards_new'
    ),
    path(
        'boards/<int:pk>/edit/',
        views.EditBoardView.as_view(),
        name='boards_edit'
    ),
    path(
        'boards/<int:pk>/delete',
        views.DeleteBoardView.as_view(),
        name='boards_delete'
    ),
    path(
        'boards/<int:pk>/',
        views.DetailBoardView.as_view(),
        name='board_detail'
    ),
    path(
        'boards/<int:pk>/cards/new',
        views.CreateCardView.as_view(),
        name='boards_cards_new'
    ),
    path(
        'cards/<int:pk>/',
        views.DetailCardView.as_view(),
        name='card_detail'
    )
]
