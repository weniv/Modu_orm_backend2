from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]

# 실무에서는 이런식으로 잘 사용하지 않습니다.
# why? Django서버는 미디어를 serving하는 프레임워크가 아니에요.
# 이미지나 영상은 nginx, apache같은 웹서버를 이용해서 서빙하거나 AWS S3같은 클라우드 서비스를 이용하는 것이 좋습니다.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
