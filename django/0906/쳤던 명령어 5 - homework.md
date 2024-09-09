```python
# 과제

# 1. Book 모델을 사용합니다.
# 2. Book 모델에 CRUD를 수행할 수 있는 뷰셋을 매핑합니다.
# 3. Book 모델은 읽기(GET, HEAD, OPTIONS)는 모두에게 허용하고, 쓰기(PUT, PATCH, DELETE, POST)는 인증된 사용자에게만 허용합니다. 그런데 쓰기 중에서도 수정(PUT, PATCH)과 삭제(DELETE)는 작성자에게만 허용합니다.

###################################

# 제출 Code
# permissions.py
# views.py를 ||```python  code ```||로 감싸서 라운지에 올려주세요.

mkdir homework
cd homework
python -m venv venv
# source venv/Scripts/activate
.\venv\Scripts\activate
pip install django djangorestframework
django-admin startproject config .
python manage.py startapp book

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
    # Local apps
    "book",
]

# 중략..

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

# 중략..

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5  # 페이지당 10개의 아이템을 보여줍니다.
}


###################################
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()

    def __str__(self):
        return self.title


###################################
# book > serializers.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'owner', 'title', 'author', 'publication_date']

###################################
# book > views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# viewset은 말 그대로 views.py에 들어가야하는 view를 모아놓은 것입니다.
# \venv\Lib\site-packages\rest_framework\viewsets.py

###################################
# config > urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]
###################################

python manage.py makemigrations
python manage.py migrate

###################################
# book > admin.py

from django.contrib import admin
from .models import Book

admin.site.register(Book)

###################################
# permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만 쓰기를 허용하는 커스텀 권한
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 객체의 author와 요청 사용자가 같은 경우에만 허용
        print(obj.owner)
        print(request.user) # 'leehojun' => 인스턴스에 __str__의 결과값이 'leehojun'
        print(request.user.username) # 'leehojun'
        # obj.owner == request.user: 객체 비교
        # obj.owner == request.user.username: 문자열 비교
        return obj.owner == request.user

###################################
# book > views.py
from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)

###################################

python manage.py createsuperuser

###################################

python manage.py runserver

# 게시물 6개 작성

###################################
요구사항
# 1. Book 모델을 사용합니다.
# 2. Book 모델에 CRUD를 수행할 수 있는 뷰셋을 매핑합니다.
# 3. Book 모델은 읽기(GET, HEAD, OPTIONS)는 모두에게 허용하고, 쓰기(PUT, PATCH, DELETE, POST)는 인증된 사용자에게만 허용합니다. 그런데 쓰기 중에서도 수정(PUT, PATCH)과 삭제(DELETE)는 작성자에게만 허용합니다.

# DRF ViewSet Thunder Client 테스트 목록

## 1. GET (목록 조회)
- URL: http://127.0.0.1:8000/books/
- 메서드: GET
- 설명: 모든 책 목록을 조회합니다. 인증이 필요 없습니다.

## 2. POST (새 항목 생성)
- URL: http://127.0.0.1:8000/books/
- 메서드: POST
- 헤더: 
  - Content-Type: application/json
  - Authorization: Basic id, password
- 바디:
    {
    "title": "hello",
    "author": "world",
    "publication_date": "2024-09-30"
    }
- 설명: 새로운 책을 생성합니다. 인증된 사용자만 가능합니다.

## 3. GET (단일 항목 조회)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: GET
- 설명: ID가 1인 책의 상세 정보를 조회합니다. 인증이 필요 없습니다.

## 4. PUT (전체 수정)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: PUT
- 헤더: 
  - Content-Type: application/json
  - Authorization: Basic id, password
- 바디:
    {
    "title": "hello!!",
    "author": "world!!",
    "publication_date": "2024-09-30"
    }
- 설명: ID가 1인 책의 모든 정보를 수정합니다. 인증된 사용자 중 작성자만 가능합니다.

## 5. PATCH (부분 수정)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: PATCH
- 헤더: 
  - Content-Type: application/json
  - Authorization: Basic id, password
- 바디:
  {
    "title": "Django for Experts"
  }
- 설명: ID가 1인 책의 제목만 수정합니다. 인증된 사용자 중 작성자만 가능합니다.

## 6. DELETE (삭제)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: DELETE
- 헤더: 
  - Authorization: Basic id, password
- 설명: ID가 1인 책을 삭제합니다. 인증된 사용자 중 작성자만 가능합니다.
```