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


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


###################################
# blog > serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content"]

###################################
# blog > views.py
from rest_framework.views import APIView
from rest_framework.response import Response
# 이 인증은 원래 simplejwt로 하는 것이 아니라, django rest framework에서 제공하는 인증 방식이었으나
# 우리가 settings.py에서 설정을 해주었기 때문에 simplejwt로 인증을 하는 것이다.
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

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import PostListView

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
# thunder client > Collections > menu > new collection
# jwt menu > new request
# jwt > export > download

{
    "clientName": "Thunder Client",
    "collectionName": "jwt",
    "collectionId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
    "dateExported": "2024-09-06T01:17:46.777Z",
    "version": "1.2",
    "folders": [],
    "requests": [
        {
            "_id": "680eb762-debf-48e4-919f-153e7512dc76",
            "colId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
            "containerId": "",
            "name": "api/posts/ 인증 없음",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 20000,
            "created": "2024-09-06T01:04:16.062Z",
            "modified": "2024-09-06T01:05:34.087Z",
            "headers": []
        },
        {
            "_id": "4c6e04db-3b93-416d-a96f-8c290cef7d4e",
            "colId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
            "containerId": "",
            "name": "api/posts/ 인증 있음(기본 인증)",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 30000,
            "created": "2024-09-06T01:06:10.893Z",
            "modified": "2024-09-06T01:06:55.053Z",
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
            "_id": "f580855a-99c1-4e29-ac9d-36f84cda26e8",
            "colId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
            "containerId": "",
            "name": "api/token/ 기본 인증으로 토큰 받기",
            "url": "http://127.0.0.1:8000/api/token/",
            "method": "POST",
            "sortNum": 40000,
            "created": "2024-09-06T01:07:12.771Z",
            "modified": "2024-09-06T01:09:14.052Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n \"username\": \"leehojun\",\n \"password\": \"dlghwns1234!\"\n}",
                "form": []
            },
            "auth": {
                "type": "basic",
                "basic": {
                    "username": "leehojun",
                    "password": "dlghwns1234!"
                }
            }
        },
        {
            "_id": "5d5c835e-10bd-4436-8fb4-821a54763f3a",
            "colId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
            "containerId": "",
            "name": "api/posts/ 인증 있음(토큰 인증)",
            "url": "http://127.0.0.1:8000/api/posts/",
            "method": "GET",
            "sortNum": 50000,
            "created": "2024-09-06T01:10:01.419Z",
            "modified": "2024-09-06T01:17:11.558Z",
            "headers": [],
            "auth": {
                "type": "bearer",
                "bearer": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NTg1NTEwLCJpYXQiOjE3MjU1ODQ5NTQsImp0aSI6IjcyMDc0Y2E2NmE1NDRhYzhiYmQyNGFiOTc1MWJjMTZhIiwidXNlcl9pZCI6MX0.yyCRXIu3f9bbMSZYV-klHbKkV238vfyZXKrpDkV-hfw"
            }
        },
        {
            "_id": "976cffaa-88f3-400d-9432-93a3ec9da26a",
            "colId": "58f00777-efcf-4d56-95f0-17ceb72a642a",
            "containerId": "",
            "name": "api/token/refresh/ 토큰 만료 후 토큰 재요청",
            "url": "http://127.0.0.1:8000/api/token/refresh/",
            "method": "POST",
            "sortNum": 60000,
            "created": "2024-09-06T01:13:09.579Z",
            "modified": "2024-09-06T01:15:02.628Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n  \"refresh\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNTY3MTM1NCwiaWF0IjoxNzI1NTg0OTU0LCJqdGkiOiJmOTExNDllMjYxZTI0NTE1YjVlZDIyZWQ5NWU2NmM4YSIsInVzZXJfaWQiOjF9.zbhoRfoxjVpOnY_S7LfpdSsE8yudaO5XebgIka6sB3k\"\n}",
                "form": []
            }
        }
    ],
    "ref": "I7ePvYCXXKPxUowunqJRo-JgwS9cUmm3_dzc8Vb9qsbpWq6lS4Z7H0ToRe60kJdEHflCW0SiMl7azTS59deSpQ"
}
