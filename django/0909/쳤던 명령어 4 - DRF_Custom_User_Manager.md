```python

# 커스텀 유저이고 매니저를 만들겁니다.

###################################

mkdir customusermanager
cd customusermanager
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

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    사용자 생성 및 관리 커스터마이징 매니저입니다. 생성할 때 로직이나 검증을 추가할 수 있습니다.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        """
        일반 사용자 생성 메서드입니다. is_staff와 is_superuser는 False로 설정됩니다. 오버라이드하여 변경할 수 있습니다.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        슈퍼유저 생성 메서드입니다. is_staff와 is_superuser는 True로 설정됩니다. 오버라이드하여 변경할 수 있습니다.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

###################################
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    사용자 관리 페이지 커스터마이징 클래스입니다. email이 필수가 되었기 때문에 username보다 앞에 배치합니다.
    """
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'birth_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

###################################
# admin.py의 상세 주석입니다.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    사용자 관리 페이지 커스터마이징 클래스입니다.
    UserAdmin을 상속받아 기본 기능을 유지하면서 커스텀 필드를 추가합니다.
    """
    # 이 관리자 클래스가 다루는 모델을 지정합니다.
    model = CustomUser

    # 사용자 목록 페이지에 표시될 필드들을 지정합니다.
    list_display = ('email', 'username', 'is_staff', 'is_active',)

    # 사용자 목록 페이지의 우측에 표시될 필터 옵션을 지정합니다.
    list_filter = ('email', 'is_staff', 'is_active',)

    # 사용자 상세 페이지에서 필드를 그룹화하여 표시하는 방식을 정의합니다.
    fieldsets = (
        # 첫 번째 그룹: 기본 정보
        (None, {'fields': ('email', 'username', 'password')}),
        # 두 번째 그룹: 권한 정보
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # 세 번째 그룹: 개인 정보
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'birth_date')}),
    )

    # 사용자 추가 페이지에서 표시될 필드들을 정의합니다.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # 'wide' 클래스를 사용하여 필드를 넓게 표시합니다.
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    # 검색 기능에 사용될 필드를 지정합니다.
    search_fields = ('email', 'username')

    # 사용자 목록의 기본 정렬 기준을 지정합니다.
    ordering = ('email',)

# CustomUser 모델을 CustomUserAdmin 설정과 함께 관리자 사이트에 등록합니다.
admin.site.register(CustomUser, CustomUserAdmin)

###################################
# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'bio', 'birth_date')
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
# email이 필수 필드이므로 CustomTokenObtainPairView가 username 대신 email을 사용합니다.
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
        user = CustomUser.objects.get(email=request.data["email"])
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
  "email": "leehojun@gmail.com",
  "password": "dlghwns1234!"
}


프로필 조회: GET 요청을 /accounts/profile/에 보냅니다 (인증 헤더 필요).
URL: http://127.0.0.1:8000/accounts/profile/
Headers:
{
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1ODQ5NTcwLCJpYXQiOjE3MjU4NDU5NzAsImp0aSI6ImM0M2Y4ZWExMmI3NjRhZjc5ZWNjN2ZhYmM5ZGE1NGVjIiwidXNlcl9pZCI6MX0.ecvgky19Isx0XqeaGCiY9egjqEFqlMQ9tb7Sp42Pi4k
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
# 좀 전과 내용이 같습니다. 순서는 상관 없습니다.
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "strongpassword123"
}

###################################
# first_name과 last_name을 시리얼라이저에서 제거하면 어떻게 되는지 확인

from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "bio",
            "birth_date",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


###################################
회원 가입: POST 요청을 /accounts/register/에 보냅니다.
URL: http://127.0.0.1:8000/accounts/register/
Body:
# 좀 전과 내용이 같습니다. 순서는 상관 없습니다.
# first_name 보내도 저장되지도 않고, 응답으로 돌아오지도 않습니다.
{
  "email": "newuser2@example.com",
  "username": "newuser2",
  "password": "strongpassword123",
  "first_name": "hello"
}
```