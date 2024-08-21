from django.shortcuts import render
from .models import Post
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            print(title, content)
            # 이미 PostForm에서 하고 있는 내용입니다.
            if title and content and title.lower() in content.lower():
                form.add_error(None, "내용에 제목을 그대로 포함할 수 없습니다.")
            # index.html에서 '제주가정말좋아'라고 입력하면 에러가 발생하는 것을 확인할 수 있습니다.
            if title == "제주가정말좋아":
                form.add_error(None, "제주는 좋은 곳입니다.")

    else:
        form = PostForm()
    return render(request, "main/index.html", {"posts": posts, "form": form})
