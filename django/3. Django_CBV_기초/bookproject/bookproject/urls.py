"""
URL configuration for bookproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books.views import MainView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from books.views import SignUpView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")), # books/로 시작하는 URL은 books 앱의 urls.py에서 처리
    path('', MainView.as_view(), name='main'), # 메인 화면을 보여줄 URL 지정
    path('login/', LoginView.as_view(template_name = 'login.html', redirect_authenticated_user=True), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)