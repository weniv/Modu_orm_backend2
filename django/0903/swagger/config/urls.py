from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularJSONAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # API 스키마 제공(yaml파일)
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # 테스트할 수 있는 UI
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),  # API 문서화를 위한 UI
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
