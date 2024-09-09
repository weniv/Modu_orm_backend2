from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"comments", views.CommentViewSet)  # 이 순서 주의해야 합니다!!
router.register(r"", views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
