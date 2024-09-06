```python
# View > APIView > generic.View > ViewSet
mkdir viewset
cd viewset
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
    'PAGE_SIZE': 3  # 페이지당 3개의 아이템을 보여줍니다.
}


###################################
from django.db import models

class Book(models.Model):
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
        fields = ['id', 'title', 'author', 'publication_date']

###################################
# book > views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

###################################
# config > urls.py

from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
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

python manage.py createsuperuser

###################################

python manage.py runserver

# 게시물 5개 작성

###################################
# thunder client > Collections > menu > new collection
# viewset menu > new request

# DRF ViewSet Thunder Client 테스트 목록

## 1. GET (목록 조회)
- URL: http://127.0.0.1:8000/books/
- 메서드: GET
- 설명: 모든 책 목록을 조회합니다.

## 2. POST (새 항목 생성)
- URL: http://127.0.0.1:8000/books/
- 메서드: POST
- 헤더: Content-Type: application/json
- 바디:
  {
    "title": "Django for Beginners",
    "author": "hojun",
    "publication_date": "2020-12-01"
  }
- 설명: 새로운 책을 생성합니다.

## 3. GET (단일 항목 조회)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: GET
- 설명: ID가 1인 책의 상세 정보를 조회합니다.

## 4. PUT (전체 수정)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: PUT
- 헤더: Content-Type: application/json
- 바디:
  {
    "title": "Django for Beginners!!",
    "author": "hojun!!",
    "publication_date": "2020-12-01"
  }
- 설명: ID가 1인 책의 모든 정보를 수정합니다.

## 5. PATCH (부분 수정)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: PATCH
- 헤더: Content-Type: application/json
- 바디:
  {
    "title": "Django for Experts"
  }
- 설명: ID가 1인 책의 제목만 수정합니다.

## 6. DELETE (삭제)
- URL: http://127.0.0.1:8000/books/1/
- 메서드: DELETE
- 설명: ID가 1인 책을 삭제합니다.


###################################

venv\Lib\site-packages\rest_framework\routers.py

###################################

# DefaultRouter URL 및 HTTP 메서드 매핑

| URL 패턴 | HTTP 메서드 | 액션 | 설명 |
|----------|-------------|------|------|
| `{prefix}/` | GET | list | 리소스 목록 조회 |
| `{prefix}/` | POST | create | 새 리소스 생성 |
| `{prefix}/{lookup}/` | GET | retrieve | 특정 리소스 상세 조회 |
| `{prefix}/{lookup}/` | PUT | update | 특정 리소스 전체 수정 |
| `{prefix}/{lookup}/` | PATCH | partial_update | 특정 리소스 부분 수정 |
| `{prefix}/{lookup}/` | DELETE | destroy | 특정 리소스 삭제 |

참고:
- `{prefix}`: URL 접두사 (예: 'books')
- router.register(r"books", BookViewSet)에서 'books'가 `{prefix}`에 해당
- `{lookup}`: 개별 리소스를 식별하는 값 (주로 'pk' 또는 'id')


###################################
# 수정과 삭제를 허락하지 않는 뷰셋을 만들고 싶다면? 택 1 하세요.
# 1번

class LimitedBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'head']

# 2번
class LimitedBookViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 권한을 설정하고 싶다!? 택 1 하세요.
# 1번
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 모든 동작 허용

# 2번(커스텀)
class ReadOnlyOrCreatePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        return False

class LimitedBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [ReadOnlyOrCreatePermission]


# 내가 쓴 글만 수정, 삭제할 수 있게 하고 싶다면?
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

        # 쓰기 권한은 객체의 소유자에게만 허용
        return obj.owner == request.user

# views.py
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


###################################

과제: 내가 쓴 글만 수정, 삭제할 수 있게 해주세요.

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
        return obj.author == request.user.username

# views.py
from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # permissions.IsAuthenticatedOrReadOnly는 DRF의 기본 권한입니다.
    # 읽기(GET, HEAD, OPTIONS)는 모든 사용자에게 허용하고, 쓰기(POST, PUT, PATCH, DELETE)는 인증된 사용자에게만 허용합니다.
    # permission_classes는 모든 클래스가 허용해야 허용됩니다. 하나라도 거부하면 거부됩니다. 리스트의 순서대로 클래스를 확인합니다.

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)

###################################