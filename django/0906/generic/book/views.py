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
