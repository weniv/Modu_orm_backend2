from django.urls import path
from .views import blog_list, csrf

urlpatterns = [
    path("", blog_list, name="postlist"),
    path("csrf/", csrf, name="csrf"),
]
