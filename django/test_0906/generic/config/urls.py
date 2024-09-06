from django.urls import path
from book.views import BookListCreateView, BookDetailView, BookCreateView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
]
