from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # posts = db
    # return HttpResponse(posts, content_type="application/json")
    print(HttpResponse("hello world"))
    print(type(HttpResponse("hello world")))
    print(render(request, "main.txt"))
    print(type(render(request, "main.txt")))
    return HttpResponse("hello world")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/1", index),
]
