from django.urls import path
from blog.views import PostListCreateView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
]
