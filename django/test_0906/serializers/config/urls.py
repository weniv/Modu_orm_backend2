from django.urls import path
from blog.views import PostListCreateView, PostDetailView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
]
