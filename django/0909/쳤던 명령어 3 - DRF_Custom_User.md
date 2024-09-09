```python

# 커스텀 유저이지만 매니저는 만들지 않을겁니다.

# 매니저를 만드는 경우는 아래와 같습니다.
# 기본 User 모델의 동작을 변경하고 싶을 때
# 사용자 생성 로직을 커스터마이즈하고 싶을 때
# USERNAME_FIELD를 변경할 때 (예: 이메일을 사용자 식별자로 사용)
# 추가적인 검증이나 처리가 필요한 경우

# 매니저를 만들지 않는 경우는 아래와 같습니다.
# 기본 User 모델의 동작을 그대로 사용해도 충분할 때
# 단순히 필드만 추가하고 싶을 때
# USERNAME_FIELD를 변경하지 않을 때

###################################

mkdir customuser
cd customuser
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
django-admin startproject config .
pip freeze > requirements.txt
python manage.py startapp accounts

####################################
# settings.py

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
]

# 중략

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

# 중략

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

AUTH_USER_MODEL = 'accounts.CustomUser'

###################################
# models.py
# \venv\Lib\site-packages\django\contrib\auth\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 기존 User 모델의 필드들을 모두 상속받습니다.
    # 추가로 원하는 필드를 정의할 수 있습니다.
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # 이 부분은 선택사항입니다. USERNAME_FIELD를 변경하고 싶다면 아래와 같이 설정할 수 있습니다.
    # USERNAME_FIELD = 'email'  # 이메일을 사용자 식별자로 사용하고 싶을 때
    # REQUIRED_FIELDS = ['username']  # createsuperuser 명령어 실행 시 요구되는 필드

    def __str__(self):
        return self.username

###################################
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # UserAdmin을 상속받아 커스텀 필드를 관리자 페이지에 표시합니다.
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('bio', 'birth_date')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

###################################
# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio', 'birth_date')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


###################################
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

###################################
# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="update_profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

###################################
# accounts/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

class ProfileView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data["username"])
        serializer = CustomUserSerializer(user)
        response.data["user"] = serializer.data
        return response


###################################

python manage.py makemigrations
python manage.py migrate

###################################

python manage.py createsuperuser
leehojun
leehojun@gmail.com
이호준1234!

###################################

python manage.py runserver

###################################

로그인: POST 요청을 /accounts/token/에 보내 토큰을 얻습니다.
URL: http://127.0.0.1:8000/accounts/token/
Body:
{
  "username": "leehojun",
  "password": "dlghwns1234!"
}


프로필 조회: GET 요청을 /accounts/profile/에 보냅니다 (인증 헤더 필요).
URL: http://127.0.0.1:8000/accounts/profile/
Headers:
{
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1ODQ4MjcyLCJpYXQiOjE3MjU4NDQ2NzIsImp0aSI6ImU4N2QwMGJlZjA3NzQxZTdhZmUyMmI4MDAzZGM4ODY0IiwidXNlcl9pZCI6MX0.ywUoVdIZMA7J1b8z_1tpncEjgTa-s93-8eQ17PjsjkA
}

프로필 수정: PUT 또는 PATCH 요청을 /accounts/profile/update/에 보냅니다 (인증 헤더 필요).
PATCH
URL: http://127.0.0.1:8000/accounts/profile/update/
Body:
{
    "bio": "new bio"
}


회원 가입: POST 요청을 /accounts/register/에 보냅니다.
URL: http://127.0.0.1:8000/accounts/register/
Body:
{
  "username": "newuser",
  "password": "strongpassword123",
  "email": "newuser@example.com",
  "first_name": "New",
  "last_name": "User"
}
```