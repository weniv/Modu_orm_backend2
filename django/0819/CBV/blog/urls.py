from django.urls import path
from . import views

# from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
# 장점: 필요한 것만 가져오고, 목록 파악 용이
# from . import views
# 장점: 가져올 것이 많을 때, 특히 유지보수를 자주하게될 경우 용이(위에를 수정할 필요가 없기 때문에)

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("new/", views.blog_new, name="blog_new"),
    path("<int:pk>/edit/", views.blog_edit, name="blog_edit"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
    path("test/", views.test, name="test"),
]
