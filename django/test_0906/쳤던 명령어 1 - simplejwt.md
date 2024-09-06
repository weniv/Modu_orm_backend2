```python
mkdir simplejwt
cd simplejwt
python -m venv venv
# source venv/Scripts/activate
.\venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt
django-admin startproject config .
python manage.py startapp blog

###################################
# config > settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    # Local apps
    "blog",
]

# 중략..

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

# 중략..

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),  # 2분마다 로그아웃이 되게해서 테스트
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

###################################
# blog > models.py

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

###################################
# blog > serializers.py

from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author"]


###################################
# blog > views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


###################################
# config > urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import PostListView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/posts/", PostListView.as_view(), name="post_list"),
]


###################################

python manage.py makemigrations
python manage.py migrate

###################################
# blog > admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

###################################

python manage.py createsuperuser

###################################

python manage.py runserver

# 게시물 3개 작성

###################################
# thunder client로 collection 생성 후 작성한 다음 export한 내용
# collection으로 run 실행

{
    "clientName": "Thunder Client",
    "collectionName": "blog",
    "collectionId": "0e9516e8-597e-4628-a268-85b304b9c28f",
    "dateExported": "2024-09-05T12:45:01.795Z",
    "version": "1.2",
    "folders": [],
    "requests": [
        {
            "_id": "1ea21fa1-7df2-42f1-99c6-d282e1ab2951",
            "colId": "0e9516e8-597e-4628-a268-85b304b9c28f",
            "containerId": "",
            "name": "api/posts/ 인증 없음",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 10000,
            "created": "2024-09-05T12:26:57.145Z",
            "modified": "2024-09-05T12:27:05.262Z",
            "headers": []
        },
        {
            "_id": "c5f2fa2e-2d52-4746-94fe-2151e6db4ec4",
            "colId": "0e9516e8-597e-4628-a268-85b304b9c28f",
            "containerId": "",
            "name": "api/posts/ 인증 있음(기본 인증)",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 20000,
            "created": "2024-09-05T12:27:43.180Z",
            "modified": "2024-09-05T12:27:58.806Z",
            "headers": [],
            "auth": {
                "type": "basic",
                "basic": {
                    "username": "leehojun",
                    "password": "dlghwns1234!"
                }
            }
        },
        {
            "_id": "a975c4ee-1029-489f-988d-9126219ea0a7",
            "colId": "0e9516e8-597e-4628-a268-85b304b9c28f",
            "containerId": "",
            "name": "api/token/ 기본 인증으로 토큰 받기",
            "url": "http://127.0.0.1:8000/api/token/",
            "method": "POST",
            "sortNum": 30000,
            "created": "2024-09-05T12:30:41.405Z",
            "modified": "2024-09-05T12:31:57.866Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n  \"username\": \"leehojun\",\n  \"password\": \"dlghwns1234!\"\n}",
                "form": []
            }
        },
        {
            "_id": "17dc08ac-e826-44be-a900-c0d93ee60d5c",
            "colId": "0e9516e8-597e-4628-a268-85b304b9c28f",
            "containerId": "",
            "name": "api/posts/ 인증 있음(토큰 인증)",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 40000,
            "created": "2024-09-05T12:32:18.399Z",
            "modified": "2024-09-05T12:33:05.028Z",
            "headers": [],
            "auth": {
                "type": "bearer",
                "bearer": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NTM5NjM3LCJpYXQiOjE3MjU1Mzk1MTcsImp0aSI6Ijc3OTUxYjBkMzFhNjQ2MzBiZDgxMDhiMGY2MjA5NjRiIiwidXNlcl9pZCI6MX0.gxxLiyu7OxYKGarhOAWakW4m1Sqq3tRBgz1AGVEI_V0"
            }
        },
        {
            "_id": "90de5626-6929-4066-8c22-9abd2019d0db",
            "colId": "0e9516e8-597e-4628-a268-85b304b9c28f",
            "containerId": "",
            "name": "api/token/refresh/ 토큰 만료 후 토큰 재요청",
            "url": "http://127.0.0.1:8000/api/token/refresh/",
            "method": "POST",
            "sortNum": 50000,
            "created": "2024-09-05T12:43:23.527Z",
            "modified": "2024-09-05T12:44:23.468Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n  \"refresh\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNTYyNTkxNywiaWF0IjoxNzI1NTM5NTE3LCJqdGkiOiIyZWE3ZWNmMGI3MGI0ZDkzOWQxYjY1N2VlYmQ3ZDdhMCIsInVzZXJfaWQiOjF9.cmNuXU_AjhWw7ylaZ1NsFvCKWTYs9DfYpHJxKv7I2BQ\"\n}",
                "form": []
            }
        }
    ],
    "ref": "Rzb5k4GYlB3_VZeNZQRm8KIK4NvIxfSDqdNbWqKQh6K9esx6Uv3nEPTDuZ45KgKcr-Jll0_xYCTGsDkO9WEOFw"
}