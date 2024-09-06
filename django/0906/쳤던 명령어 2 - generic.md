```python
# View > APIView > generic.View > ViewSet
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
# venv > Lib > site-packages > rest_framework > generics.py


class GenericAPIView(views.APIView):
    """
    Base class for all other generic views.
    """
    queryset = None
    serializer_class = None
    lookup_field = 'pk'
    lookup_url_kwarg = None
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def __class_getitem__(cls, *args, **kwargs):
        return cls

    def get_queryset(self):
        pass

    def get_object(self):
        pass

    def get_serializer(self, *args, **kwargs):
        pass

    def get_serializer_class(self):
        pass

    def get_serializer_context(self):
        pass

    def filter_queryset(self, queryset):
        pass

    @property
    def paginator(self):
        pass

    def paginate_queryset(self, queryset):
        pass

    def get_paginated_response(self, data):
        pass


# Concrete view classes that provide method handlers
# by composing the mixin classes with the base view.

class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin,
                     GenericAPIView):
    """
    Concrete view for deleting a model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             GenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
# thunder client > Collections > menu > new collection
# generic menu > new request
# generic > export > download

{
    "clientName": "Thunder Client",
    "collectionName": "generic",
    "collectionId": "791c1fa3-b411-48b1-b444-1db19b94d96e",
    "dateExported": "2024-09-06T02:18:07.364Z",
    "version": "1.2",
    "folders": [],
    "requests": [
        {
            "_id": "b854de3b-d300-4afe-a104-49f50a4aabcc",
            "colId": "791c1fa3-b411-48b1-b444-1db19b94d96e",
            "containerId": "",
            "name": "Read",
            "url": "http://127.0.0.1:8000/books/",
            "method": "GET",
            "sortNum": 20000,
            "created": "2024-09-06T02:08:55.456Z",
            "modified": "2024-09-06T02:08:59.431Z",
            "headers": []
        },
        {
            "_id": "8b60465d-e397-4760-83cd-76138f953388",
            "colId": "791c1fa3-b411-48b1-b444-1db19b94d96e",
            "containerId": "",
            "name": "Read Copy",
            "url": "http://127.0.0.1:8000/books/",
            "method": "GET",
            "sortNum": 25000,
            "created": "2024-09-06T02:17:06.278Z",
            "modified": "2024-09-06T02:17:06.278Z",
            "headers": []
        },
        {
            "_id": "b374d9bb-3efc-4b8f-a68b-6581044193eb",
            "colId": "791c1fa3-b411-48b1-b444-1db19b94d96e",
            "containerId": "",
            "name": "Create",
            "url": "http://127.0.0.1:8000/books/create/",
            "method": "POST",
            "sortNum": 40000,
            "created": "2024-09-06T02:14:23.980Z",
            "modified": "2024-09-06T02:15:47.651Z",
            "headers": [],
            "body": {
                "type": "json",
                "raw": "{\n  \"title\": \"test123123\",\n  \"author\": \"test123123\",\n  \"publication_date\": \"2030-09-09\"\n}",
                "form": []
            }
        },
        {
            "_id": "24ca2f6a-88ec-42e9-9b7f-76c24d716b37",
            "colId": "791c1fa3-b411-48b1-b444-1db19b94d96e",
            "containerId": "",
            "name": "Detail Read",
            "url": "http://127.0.0.1:8000/books/1",
            "method": "GET",
            "sortNum": 50000,
            "created": "2024-09-06T02:12:20.631Z",
            "modified": "2024-09-06T02:17:23.808Z",
            "headers": []
        }
    ],
    "ref": "2i3St6uehOSW2d5mL5DnSUEXp3B_IwdBNH5Vi2wNRnjXzjV89h3mWDzzZ0ZdlyrEZbbWDJ-ojjHcAacaeVxxSQ"
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

```