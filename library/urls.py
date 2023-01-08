"""Url Pages"""

# Libraries
from django.urls import path

# Views
from . import views


app_name = 'library'
urlpatterns = [
    path('', views.LibraryView.as_view(), name='home'),
    path("books/new", views.BookNewView.as_view(), name="new_book"),
    path('books/<int:pk>/edit', views.BookEditView.as_view(), name='edit_book'),
    path('books/<int:pk>/delete', views.delete_book, name='delete_book'),
    path("books/<int:pk>/send_to_kindle", views.send_to_kindle, name="send_to_kindle"),
    path("books/<int:pk>/download_file", views.download_file, name="download_file"),

    path("genres", views.BookGenresListView.as_view(), name="list_genres"),
    path("genres/new", views.BookGenreNewView.as_view(), name="new_genre"),
    path('genres/<int:pk>/edit', views.BookGenderEditView.as_view(), name='edit_genre'),
    path('genres/<int:pk>/delete', views.delete_book_genre, name='delete_book_genre'),

    path("authors", views.AuthorsListView.as_view(), name="list_authors"),
    path("authors/new", views.AuthorNewView.as_view(), name="new_author"),
    path('authors/<int:pk>/edit', views.AuthorEditView.as_view(), name='edit_author'),
    path('authors/<int:pk>/delete', views.delete_author, name='delete_author'),
]
