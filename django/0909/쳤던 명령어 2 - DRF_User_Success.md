```python

mkdir user_one_to_one_success
cd user_one_to_one_success
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

python manage.py createsuperuser
leehojun
leehojun@gmail.com
이호준1234!

###################################

python manage.py runserver

###################################

# 애러 없이 들어온 것을 확인할 수 있음!

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