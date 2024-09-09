```python

# AbstractBaseUser를 상속받아 만듭니다.
# AbstractBaseUser는 기본적으로 create_user()와 create_superuser() 메서드를 제공하지 않습니다. 이 메서드들은 Django의 명령어 createsuperuser와 admin 인터페이스에서 사용됩니다.
# 따라서 별도로 만들어야 합니다.


###################################

mkdir custombaseusermanager
cd custombaseusermanager
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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    커스텀 유저 모델을 위한 매니저 클래스입니다.
    이 클래스는 새 사용자를 생성하는 메서드를 제공합니다.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        """
        일반 사용자를 생성하는 메서드입니다.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)  # 이메일 정규화
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)  # 사용자를 데이터베이스에 저장
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        관리자(superuser) 사용자를 생성하는 메서드입니다.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # 관리자는 반드시 is_staff와 is_superuser가 True여야 합니다.
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    커스텀 유저 모델 클래스입니다.
    AbstractBaseUser를 상속받아 기본 인증 기능을 제공받고,
    PermissionsMixin을 상속받아 Django의 권한 시스템을 사용합니다.
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)  # 관리자 사이트 접근 권한
    is_active = models.BooleanField(default=True)  # 계정 활성화 상태
    date_joined = models.DateTimeField(default=timezone.now)  # 가입 일자
    bio = models.TextField(max_length=500, blank=True)  # 자기소개
    birth_date = models.DateField(null=True, blank=True)  # 생년월일

    objects = CustomUserManager()  # 커스텀 매니저 지정

    USERNAME_FIELD = 'email'  # 로그인에 사용할 필드 지정
    REQUIRED_FIELDS = ['username']  # createsuperuser 명령어 실행 시 요구되는 필드

    class Meta:
        """
        관리자 페이지 등에서 보여질 단수이름, 복수이름을 지정합니다.
        """
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email  # 객체를 문자열로 표현할 때 이메일 반환

###################################
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('bio', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
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
# accounts/serializers.py
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
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1Nzk3Mjk1LCJpYXQiOjE3MjU3OTM2OTUsImp0aSI6IjRkZDI0NThlZWZhZTRkNmQ4NzE0NDAxN2FlMjAxNWE4IiwidXNlcl9pZCI6MX0.EylezSlDlABRTYqYACdyP0WkJUg8FjPjJs3eAn-TjG4
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
  "password": "strongpassword123",
  "first_name": "New",
  "last_name": "User"
}

###################################
# 과제: 아래 파일을 수정해서 hompage_url을 슈퍼 유저를 만들 때 생성하도록 하고, 일반 유저를 만들 때에도 생성되게 해주세요. 이어서 한 번 해보도록 하겠습니다.
# 시간은 15분 드리겠습니다.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, homepage_url, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not homepage_url:
            raise ValueError(_('The Homepage URL field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, homepage_url=homepage_url, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, homepage_url, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, homepage_url, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    homepage_url = models.URLField(_('homepage URL'), max_length=200)  # 새로 추가된 필수 필드
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'homepage_url']  # homepage_url 추가

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

###################################
# serializers.py
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
            "homepage_url", # 추가
            "password",
            "bio",
            "birth_date",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


###################################

python manage.py makemigrations

 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.

1번 선택

>>> 'http://example.com'

###################################
회원 가입: POST 요청을 /accounts/register/에 보냅니다.
URL: http://127.0.0.1:8000/accounts/register/
Body:
{
  "email": "newuser@example.com",
}

# Response
{
  "username": [
    "이 필드는 필수 항목입니다."
  ],
  "homepage_url": [
    "이 필드는 필수 항목입니다."
  ],
  "password": [
    "이 필드는 필수 항목입니다."
  ]
}

###################################

http://127.0.0.1:8000/accounts/register/
{
    "email": "newuser@example.com",
    "username": "newuser",
    "homepage_url": "http://example.com",
    "password": "strongpassword123"
}
```