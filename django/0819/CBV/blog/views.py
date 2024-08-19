from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Post
from django.db.models import Q

# 클래스 기반 뷰가 꼭 제네릭 뷰는 아닙니다.
# 클래스로 HttpResponse를 반환하게 하면 그것도 클래스 기반 뷰입니다.
# 실무에서는 클래스 기반 뷰를 제네릭 뷰라고 부르는 경우가 많습니다.
# 제네릭 뷰는 장고에서 제공하는 여러가지 기능을 미리 구현해 놓은 클래스 기반 뷰입니다.


class PostList(ListView):
    model = Post
    ordering = "-created_at"  # "-pk"도 가능
    # template_name = "blog/내가_원하는_파일명.html" # default: blog/post_list.html
    # context_object_name = "posts" # default: object_list
    # paginate_by = 5 # 페이지네이션(한 페이지에 몇 개를 보여줄지)

    def get_queryset(self):
        """
        get_queryset은 템플릿에서 사용할 {{object_list}}를 만드는 함수입니다.
        일반적으로는 Post.objects.all()과 같은 역할을 합니다.
        그런데 우리는 특수한 코드 분기를 위해 이 함수를 오버라이딩(재정의)합니다.

        127.0.0.1:8000 GET 이걸로 들어오게 되면?
        127.0.0.1:8000?q=hello GET 이걸로 들어오게 되면?
        127.0.0.1:8000?q=hello&name=hojun GET 이걸로 들어오게 되면?
        """
        queryset = super().get_queryset()  # Post.objects.all()과 같은 역할을 합니다.
        # 템플릿에서는 {{object_list}}로 사용할 수 있습니다.
        q = self.request.GET.get("q", "")  # q라는 이름으로 GET 요청을 받습니다.
        if q:
            # q의 값을 가지고 있는 데이터를 추출합니다.
            # queryset = queryset.filter(title__icontains=q)
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            ).distinct()
        return queryset


class PostDetail(DetailView):
    model = Post
    # template_name = "blog/내가_원하는_파일명.html" # default: blog/post_detail.html
    # context_object_name = "post" # default: object


class PostCreate(CreateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("blog_list")  # 성공했을 때 이동할 URL
    # fields = ["title", "content", "author"] # 이렇게 필드를 지정해줄 수도 있다.
    # template_name = "blog/내가_원하는_파일명.html" # default: blog/post_form.html
    # success_url = "/blog/" # default: reverse_lazy("blog_list")
    # reverse_lazy("blog_list")를 하는 이유는 object가 생성이 되고 나서 url로 이동해야 하는데 reverse는 함수이기 때문에 함수가 실행되는 시점에 url로 이동하게 되어버린다. 그래서 post가 생성된 후에 url로 이동하게 하기 위해서 기다리겠다는 함수가 reverse_lazy를 사용한다.


class PostUpdate(UpdateView):
    model = Post
    fields = "__all__"  # "__all__"도 가능
    success_url = reverse_lazy("blog_list")  # 성공했을 때 이동할 URL
    # template_name = "blog/내가_원하는_파일명.html" # default: blog/post_form.html
    # success_url = "/blog/" # default: reverse_lazy("blog_list")


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy("blog_list")  # 성공했을 때 이동할 URL
    # template_name = "blog/내가_원하는_파일명.html" # default: blog/post_confirm_delete.html
    # success_url = "/blog/" # default: reverse_lazy("blog_list")
    # 삭제되고 다 완료되지 않은 상태에서 blog_list로 넘어가지 않도록 하기 위해서 reverse_lazy를 사용합니다.


class PostTest(CreateView):
    model = Post

    # 메서드 오버라이딩(CreateView의 메서드를 재정의)
    def get(self, request):
        return HttpResponse("get 요청이 왔습니다.")

    def post(self, request):
        return HttpResponse("post 요청이 왔습니다.")


# 아래와 같이 사용하진 않고, urls.py에서 as_view()를 사용하여 사용하는 경우가 많습니다.
blog_list = PostList.as_view()
blog_detail = PostDetail.as_view()
blog_new = PostCreate.as_view()
blog_edit = PostUpdate.as_view()
blog_delete = PostDelete.as_view()
test = PostTest.as_view()
