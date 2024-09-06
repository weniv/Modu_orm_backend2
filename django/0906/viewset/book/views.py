from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# viewset은 말 그대로 views.py에 들어가야하는 view를 모아놓은 것입니다.
# \venv\Lib\site-packages\rest_framework\viewsets.py
