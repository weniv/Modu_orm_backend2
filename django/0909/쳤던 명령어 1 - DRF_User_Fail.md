```python
(실습) OneToOneField를 사용한 Profile 모델: Django의 인증 시스템과 완벽하게 호환, 추가 필드 관리 용이
    - 필요 없는 공간의 낭비 < 유연한 확장의 가치 (트레이드 오프, 하나를 얻으면 하나를 잃는다!)
    - 실제 사용자 데이터는 그리 큰 데이터를 차지 하지 않음
    - third party 앱들과의 호환성을 걱정할 필요가 없음
    - 마이그레이션에서 문제가 발생하지 않음
    - 프로젝트 진행 중에도 필요에 따라 필드 추가 가능
    - User 모델과 Profile 모델을 별도로 관리해야 하는 번거로움 존재

기본 User 모델 사용: Django의 기본 User 모델을 그대로 사용
    - 마이그레이션에서 문제가 발생하지 않음
    - 이렇게 사용해도 된다면 이 방법이 가장 안전하고 간단
    - 추가 필드가 필요 없는 간단한 프로젝트에 적합
    - Django의 모든 기능과 완벽하게 호환

(실습) AbstractUser를 사용한 커스텀 User 모델: User 모델을 확장하고 싶을 때 사용
    - third party 앱들과의 호환성 문제가 발생할 수 있음
    - 기본 User 모델의 모든 필드와 기능을 그대로 유지하면서 새 필드 추가 가능
    - 프로젝트 시작 시 결정해야 함 (나중에 변경 시 복잡한 마이그레이션 필요)

(실습) AbstractBaseUser를 사용한 커스텀 User 모델: User 모델을 완전히 새로 만들고 싶을 때 사용
    - 가장 유연한 방법이지만 구현이 복잡함
    - 인증 관련 필드와 메서드를 직접 구현해야 함
    - 특별한 인증 요구사항이 있는 프로젝트에 적합

Proxy 모델: 기존 User 모델의 동작을 변경하고 싶지만 데이터베이스 테이블은 그대로 유지하고 싶을 때 사용
    - 데이터베이스 스키마 변경 없이 모델의 동작만 수정 가능
    - 새 필드 추가는 불가능하며, 메서드 추가나 수정만 가능
    - 특정 User 그룹에 대한 별도의 동작을 정의할 때 유용

###################################
# Proxy 모델
# 별도의 서버를 구축하는 것이 아닌 기존 User를 활용

class Student(User):
    objects = StudentManager()

    @property
    def grade(self):
        # 학년을 계산하는 로직
        return "1학년"  # 예시로 고정값 반환

    class Meta:
        proxy = True
        ordering = ['username']

###################################

# User를 만들기로 선택했으면 Manager를 함께 만들어야 합니다.
# 만약 User를 만들면 Profile과 1:1 관계를 유지할 필요 없이 새로운 User에 필드를 추가하면 됩니다.
# 이 예제는 한 번은 겪에될 애러에 관한 예제입니다.
# 따라서 User를 만드는 작업과 Manager 작업은 migrations를 하기 전 진행하세요.

###################################
# 실수: migrate를 먼저 해버린 것이 실수입니다.

mkdir user_one_to_one_fail
cd user_one_to_one_fail
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
django-admin startproject config .
python manage.py migrate
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

###################################
# 실수: createsuperuser를 먼저 해버린 것이 실수입니다.

python manage.py createsuperuser
leehojun
leehojun@gmail.com
이호준1234!

###################################
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    receiver 데커레이터는 User 모델이 저장될 때마다 호출되는 함수, view에서 유효성 검사를 진행하고 save()를 호출하면 이 함수가 호출됩니다. 유효성 검사를 실행하진 않습니다. 함수이름은 자유롭게 지정할 수 있습니다.
    """
    if created: # User가 생성되었을 때
        Profile.objects.create(user=instance)
    # 유저가 변경되었을 때
    instance.profile.save()


###################################
# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source="profile.bio", required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "bio")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance = super().update(instance, validated_data)

        if profile_data:
            instance.profile.bio = profile_data.get("bio", instance.profile.bio)
            instance.profile.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "bio")

    def create(self, validated_data):
        bio = validated_data.pop("bio", "")
        user = User.objects.create_user(**validated_data)
        user.profile.bio = bio
        user.profile.save()
        return user


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
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer, RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        serializer = UserProfileSerializer(user)
        response.data["user"] = serializer.data
        return response


###################################

python manage.py makemigrations
python manage.py migrate

###################################

python manage.py runserver

###################################

# http://127.0.0.1:8000/admin/ 에서 Superuser의 Profile 입력

###################################

# http://127.0.0.1:8000/admin/ 에 접속도 안됨!
# 아래와 같은 애러 발생

RelatedObjectDoesNotExist at /admin/login/
User has no profile.

###################################
# 이 애러는 반드시 한 번 만나게 되어 있습니다.
# Profile은 1:1 필드로 User와 연결되어 있기 때문에 User가 생성될 때 Profile도 함께 생성되어야 합니다.

1. 처음 슈퍼 유저를 생성할 때 프로필을 입력 받도록 수정했으면 되는 것 아니냐?
=> BaseUserManager와 같은 방법으로 처음에 등록을 할 때 일반 유저와 슈퍼 유저의 가입을 구분하여 프로필을 입력 받도록 수정하면 됨.

2. superuser는 admin에서 손보거나 Django shell에서 손보고, 일반 유저만 프로필을 입력해야만 가입할 수 있도록 수정

###################################
# 아래 방법은 임시 방편입니다. User를 생성할 때 자동을 Profile을 생성하는 방법이 가장 좋습니다.

python manage.py shell

from django.contrib.auth.models import User
from accounts.models import Profile

# username이 'leehojun'인 User 객체를 데이터베이스에서 가져옵니다.
# 만약 해당 사용자가 존재하지 않으면 DoesNotExist 예외가 발생합니다.
user = User.objects.get(username='leehojun')

# Profile.objects.get_or_create() 메서드를 사용하여 user에 대한 Profile을 가져오거나 생성합니다.
# 이 메서드는 (object, created) 형태의 튜플을 반환합니다.
# - object: 가져오거나 생성된 Profile 객체
# - created: 객체가 새로 생성되었으면 True, 기존에 존재하던 객체를 가져왔으면 False
# 이 경우 반환값을 변수에 할당하지 않았으므로, 결과를 확인할 수 없지만 작업은 수행됩니다.
Profile.objects.get_or_create(user=user) 
exit()

###################################

# 이제 admin 페이지에 접속할 수 있습니다.
# 다만 아직 Profile을 수정할 수 없습니다.

###################################
# account/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


###################################

# 다시 admin 페이지에 접속하여 User와 Profile을 확인해보세요.

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
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1Nzg5Mjg5LCJpYXQiOjE3MjU3ODU2ODksImp0aSI6ImY4NjMxZGU2ZGU3NTRiNjlhZmQ5MTBmN2JhNDE2ZTcwIiwidXNlcl9pZCI6MX0.Gf9L8bfgSIsUIC8BepwUqAGGVWuUUCFcVnZFHV9LKPM
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