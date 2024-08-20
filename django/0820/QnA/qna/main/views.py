from django.shortcuts import render
from .models import Post


def index(request):
    post = Post.objects.get(pk=2)  # 아까 delete해서 pk=1이 없어져서 pk=2로 변경
    return render(request, "main/index.html", {"post": post})
