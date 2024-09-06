```python
mkdir generic
cd generic
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
    'PAGE_SIZE': 10  # 페이지당 10개의 아이템을 보여줍니다.
}


###################################
# book > models.py

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
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    이 뷰는 책 목록을 조회(GET)하고 새 책을 생성(POST)하는 API를 제공합니다.
    
    ListCreateAPIView는 다음 두 가지 기능을 결합합니다:
    1. ListAPIView: 모델의 쿼리셋을 기반으로 객체 목록을 반환합니다.
    2. CreateAPIView: 새로운 객체를 생성합니다.

    장점:
    - 코드 중복을 줄입니다: GET과 POST 메소드를 한 클래스에서 처리합니다.
    - 자동으로 적절한 HTTP 메소드를 처리합니다.
    - 페이지네이션, 필터링 등의 기능을 쉽게 추가할 수 있습니다.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveAPIView):
    """
    이 뷰는 특정 책의 상세 정보를 조회(GET)하는 API를 제공합니다.
    
    RetrieveAPIView는 단일 객체의 세부 정보를 반환합니다.

    장점:
    - URL에서 객체의 primary key를 자동으로 처리합니다.
    - 객체가 존재하지 않을 경우 자동으로 404 응답을 반환합니다.
    - 권한 체크, 쿼리 최적화 등을 쉽게 구현할 수 있습니다.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    """
    이 뷰는 새로운 책을 생성(POST)하는 API를 제공합니다.
    
    CreateAPIView는 새로운 객체 생성에 특화된 뷰입니다.

    장점:
    - 객체 생성 로직을 간소화합니다.
    - 자동으로 생성된 객체의 위치(URL)를 응답 헤더에 포함시킵니다.
    - 유효성 검사와 에러 처리를 자동으로 수행합니다.
    """
    serializer_class = BookSerializer


###################################
# config > urls.py

from django.urls import path
from book.views import BookListCreateView, BookDetailView, BookCreateView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
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

# 게시물 12개 작성

###################################
# thunder client로 collection 생성 후 작성한 다음 export한 내용
# collection으로 run 실행

{
    "clientName": "Thunder Client",
    "collectionName": "book",
    "collectionId": "07c73317-7845-4727-a41e-90f1aa1c3eab",
    "dateExported": "2024-09-05T13:38:12.900Z",
    "version": "1.2",
    "folders": [],
    "requests": [
        {
            "_id": "d19f2569-81b4-471d-b44e-76324ff63641",
            "colId": "07c73317-7845-4727-a41e-90f1aa1c3eab",
            "containerId": "",
            "name": "read",
            "url": "http://127.0.0.1:8000/books/?page=2",
            "method": "GET",
            "sortNum": 10000,
            "created": "2024-09-05T13:33:56.310Z",
            "modified": "2024-09-05T13:34:50.974Z",
            "headers": [],
            "params": [
                {
                    "name": "page",
                    "value": "2",
                    "isPath": false
                }
            ]
        },
        {
            "_id": "bd2761b9-a062-4e0f-911f-8430d2fc5bd7",
            "colId": "07c73317-7845-4727-a41e-90f1aa1c3eab",
            "containerId": "",
            "name": "create",
            "url": "http://127.0.0.1:8000/books/create/",
            "method": "POST",
            "sortNum": 20000,
            "created": "2024-09-05T13:35:14.251Z",
            "modified": "2024-09-05T13:36:54.676Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n  \"title\": \"test123\", \n  \"author\": \"test123\", \n  \"publication_date\": \"2024-09-09\"\n}",
                "form": []
            }
        },
        {
            "_id": "631c6e21-bc78-49f7-9c48-e24dd25b3a4e",
            "colId": "07c73317-7845-4727-a41e-90f1aa1c3eab",
            "containerId": "",
            "name": "detail",
            "url": "http://127.0.0.1:8000/books/1",
            "method": "GET",
            "sortNum": 30000,
            "created": "2024-09-05T13:37:30.579Z",
            "modified": "2024-09-05T13:37:48.296Z",
            "headers": []
        }
    ],
    "ref": "Xsif0birMoWCGKpib7rVWH81iuwH3yxS1ODiRSpqLfUPVndPQGUSx8pQvMTuI3r6Q5DzstBNKSYQmWZTpkED_Q"
}

###################################
# 비교만 해보세요.
# 실제 작성하는 코드는 아닙니다.

# Generic Views를 사용한 경우

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Generic Views를 사용하지 않은 경우

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class BookListCreateView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)