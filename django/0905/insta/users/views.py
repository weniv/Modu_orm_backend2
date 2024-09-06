# users > views.py

# Basic Django Modules
from django.contrib.auth import get_user_model

# Rest Framework Modules
from rest_framework import generics
from rest_framework import permissions

# Models
from .serializers import UserSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    # CreateAPIView는 post요청을 받아서 새로운 user를 만들어주는 역할을 합니다.
    # CreateAPIView는 post요청을 받으면 201 Created를 반환합니다.
    # CreateAPIView는 get, put, patch, delete 등 허용되지 않은 요청을 받으면 405 Method Not Allowed를 반환합니다.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 모든 사용자 접근 가능
    # permission_classes = [permissions.IsAuthenticated, ]
    # permission_classes = [permissions.IsAdminUser, ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    # 모든 사용자가 접근 가능하도록 설정합니다.
    # settings.py에 REST_FRAMEWORK의 DEFAULT_PERMISSION_CLASSES를 덮어쓰기 하기 위해서는 아래와 같이 설정합니다.
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView: GET을 지원
    RetrieveUpdateAPIView: GET과 PUT/PATCH를 지원
    RetrieveDestroyAPIView: GET과 DELETE를 지원
    RetrieveUpdateDestroyAPIView: GET, PUT/PATCH, DELETE를 모두 지원
    """

    # RetrieveAPIView는 get요청을 받아서 user의 정보를 반환해주는 역할을 합니다.
    # RetrieveAPIView는 get요청을 받으면 200 OK를 반환합니다.
    queryset = User.objects.all()
    serializer_class = UserSerializer
