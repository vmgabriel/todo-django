# Libraries
from __future__ import annotations
import os
import mimetypes

from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django.conf import settings
from . import models, filters, forms, tasks
from custom_widgets.list import basic as list_basic, list_object
from custom_widgets import fields

# Books
class LibraryView(LoginRequiredMixin, FilterView):
    """The Main Page"""
    model = models.Books
    paginate_by = settings.PAGINATION_LIMIT
    template_name = 'library/index.html'
    filterset_class = filters.BooksFilter

    def get_queryset_with_filter(self):
        queryset = self.get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        return context

class BookNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'library/book/edit.html'
    form_class = forms.BookForm
    success_url = "library:home"
    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(BookNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        self.object.genres.set(form.cleaned_data['genres'])
        self.object.authors.set(form.cleaned_data['authors'])
        tasks.conversion_book.apply_async(args=(self.object.pk,))
        return redirect(self.get_success_url())

class BookEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Books
    form_class = forms.BookForm
    template_name = 'library/book/edit.html'
    success_url = 'library:home'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(BookEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.genres.set(form.cleaned_data['genres'])
        self.object.authors.set(form.cleaned_data['authors'])
        self.object.save()
        return redirect(
            self.get_success_url()
        )

# Book Genres
class BookGenresListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = models.BookGenres
    filterset_class = filters.BookGenreFilter
    template_name = "library/genre/index.html"
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "library:new_genre"
    url_delete = "library:edit_genre"
    url_edit = "library:delete_book_genre"
    title_form = "Book Genres"
    fields_to_show: list[list_object.ListComponent] = [
        list_object.ListComponent(
            "name",
            "Name",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "description",
            "Description",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "color",
            "Color",
            fields.Field.COLOR,
        ),
    ]

class BookGenreNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = "library/genre/edit.html"
    form_class = forms.BookGenreForm
    success_url = "library:new_genre"
    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(BookGenreNewView, self).get_context_data(**kwargs)
        context["mode"] = "Save"
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())

class BookGenderEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.BookGenres
    form_class = forms.BookGenreForm
    template_name = 'library/genre/edit.html'
    success_url = 'library:list_genres'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(BookGenderEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.save()
        return redirect(
            self.get_success_url()
        )


# Authors
class AuthorsListView(LoginRequiredMixin, list_basic.ListBasicMixin):
    model = models.Authors
    paginate_by = settings.PAGINATION_LIMIT
    template_name = "library/author/index.html"
    filterset_class = filters.AuthorFilter
    fields_back = {}
    fields_in_url = {"pk": "object.id"}
    url_create = "library:new_author"
    url_delete = "library:delete_author"
    url_edit = "library:edit_author"
    title_form = "Authors"
    fields_to_show: list[list_object.ListComponent] = [
        list_object.ListComponent(
            "image",
            "Image",
            fields.Field.IMAGE,
        ),
        list_object.ListComponent(
            "name",
            "Name",
            fields.Field.STRING,
        ),
        list_object.ListComponent(
            "description",
            "Description",
            fields.Field.STRING,
        ),
    ]

    def get_queryset_with_filter(self):
        queryset = self.get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_queryset(self, *args, **kwargs):
        queryset = super(AuthorsListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True)
        return queryset

class AuthorNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'library/author/edit.html'
    form_class = forms.AuthorForm
    success_url = "library:new_author"
    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(AuthorNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())

class AuthorEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Authors
    form_class = forms.AuthorForm
    template_name = 'library/author/edit.html'
    success_url = 'library:list_authors'

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(AuthorEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.save()
        return redirect(
            self.get_success_url()
        )


# Removal methods
@login_required
def delete_book_genre(request, pk):
    model = models.BookGenres
    genre: model = get_object_or_404(model, pk=pk)
    genre.enabled = False
    genre.save()
    return redirect("library:list_genres")


@login_required
def delete_author(request, pk):
    model = models.Authors
    author: model = get_object_or_404(model, pk=pk)
    author.enabled = False
    author.save()
    return redirect("library:list_authors")


@login_required
def delete_book(request, pk):
    model = models.Books
    book: model = get_object_or_404(model, pk=pk)
    book.enabled = False
    book.save()
    return redirect("library:home")


@login_required
def send_to_kindle(request, pk: int):
    model = models.Books
    book: model = get_object_or_404(model, pk=pk)
    user = request.user
    if user.kindle_email is not None and book.file_mobi is not None:
        tasks.send_book.apply_async(args=(
            [user.kindle_email],
            book.file_mobi.name.split("/")[-1]
        ))
    return redirect("library:home")

@login_required
def download_file(request, pk: int):
    model = models.Books
    book: model = get_object_or_404(model, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, book.file.name)
    mime_type, _ = mimetypes.guess_type(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
