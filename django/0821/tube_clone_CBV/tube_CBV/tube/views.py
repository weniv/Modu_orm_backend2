from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    CreateView,
)
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post


post_list = PostListView.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("tube:post_list")
    template_name = "tube/form.html"

    def form_valid(self, form):
        video = form.save(commit=False)  # commit=False는 DB에 저장하지 않고 객체만 반환
        video.author = self.request.user
        return super().form_valid(form)  # 이렇게 호출했을 때 저장합니다.


post_new = PostCreateView.as_view()


class PostDetailView(DetailView):
    model = Post
    # context_object_name = 'licat_objects' # {{licat_objects.title}} 이런식으로 사용 가능

    def get_context_data(self, **kwargs):
        """
        여기서 원하는 쿼리셋이나 object를 추가한 후 템플릿으로 전달할 수 있습니다.
        """
        context = super().get_context_data(**kwargs)
        print("------------")
        print(context)
        print(type(context))
        print(dir(context))
        context["value"] = "hello world"
        print(context)
        print("------------")
        return context


post_detail = PostDetailView.as_view()


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("tube:post_list")
    template_name = "tube/form.html"

    def test_func(
        self,
    ):  # UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩, True, False 값으로 접근 제한
        return self.get_object().author == self.request.user


post_edit = PostUpdateView.as_view()


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("tube:post_list")

    def test_func(
        self,
    ):  # UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩, True, False 값으로 접근 제한
        return self.get_object().author == self.request.user


post_delete = PostDeleteView.as_view()
