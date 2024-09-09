```python
###################################
# 목표
앞서 배운 user 모델 구현 방법과 ViewSet을 사용하여 API를 구현할 수 있다.

###################################

ViewSet에서 주의할 점: URL 패턴을 정의할 때!
   - ViewSet의 메서드 이름을 사용하여 URL 패턴을 생성하기 때문에, ViewSet 클래스 내부의 메서드 이름을 변경하면 URL 패턴도 함께 변경되어야 함
   - URL 정의 순서에 따라 상위 URL 패턴이 하위 URL 패턴을 가로채는 문제가 발생할 수 있음. 이를 방지하기 위해 URL 패턴을 정의할 때는 순서에 주의하여야 함.

###################################
URL 설계

# accounts
POST    /accounts/token/ # 토큰 발급
POST    /accounts/accounts/register/ # 회원가입
GET     /accounts/profile/ # 내 정보 조회 - 로그인한 사용자
PATCH   /accounts/profile/update # 내 정보 수정 - 로그인한 사용자

# posts
GET     /posts/ # 포스트리스트 - 로그인 안한 사용자도 볼 수 있도록
GET     /posts/{id}/ # 포스트 상세(댓글, 좋아요) - 로그인한 사용자
GET     /posts/{post_id}/comments/ # 해당 포스트에 댓글 리스트 - 로그인한 사용자
POST    /posts/{post_id}/like/ # 좋아요 생성 - 로그인한 사용자
DELETE  /posts/{post_id}/like/ # 좋아요 삭제 - 로그인한 사용자
POST    /posts/comments/ # 댓글 생성 - 로그인한 사용자
POST    /posts/write/ # 포스트 작성 - 로그인한 사용자

###################################

# 과제입니다. 1시간동안 해당 URL을 구현해주세요.

###################################
# user 설계
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
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
# DB 설계

# posts > models.py
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

###################################

mkdir api
cd api
python -m venv venv
.\venv\Scripts\activate
pip install django pillow djangorestframework djangorestframework-simplejwt django-cors-headers
django-admin startproject config .
pip freeze > requirements.txt
python manage.py startapp accounts
python manage.py startapp posts

###################################

# django-cors-headers는 이 프로젝트에 필요하지 않지만
# 나중에 여러분이 .html을 live server로 테스트 할 때 필요합니다.
# 테스트 해보세요.

###################################

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps
    'accounts',
    'posts',
    # third party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware", # 추가
]

##

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

##

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

##

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
# config > urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    # path("posts/", include("posts.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

###################################

accounts app 작성

###################################
# accounts > models.py

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
leehojun
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

posts app 작성

###################################
# config > urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


###################################
# posts > urls.py
# \venv\Lib\site-packages\rest_framework\routers.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet) # 이 순서 주의해야 합니다!!
router.register(r'', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

###################################

# DefaultRouter URL 및 HTTP 메서드 매핑
| URL 패턴             | HTTP 메서드  | 액션(메서드명)  | 설명 |
|----------------------|-------------|----------------|------|
| `{prefix}/`          | GET         | list           | 리소스 목록 조회 |
| `{prefix}/`          | POST        | create         | 새 리소스 생성 |
| `{prefix}/{lookup}/` | GET         | retrieve       | 특정 리소스 상세 조회 |
| `{prefix}/{lookup}/` | PUT         | update         | 특정 리소스 전체 수정 |
| `{prefix}/{lookup}/` | PATCH       | partial_update | 특정 리소스 부분 수정 |
| `{prefix}/{lookup}/` | DELETE      | destroy        | 특정 리소스 삭제 |

참고:
- `{prefix}`: URL 접두사 (예: 'books')
- router.register(r"books", BookViewSet)에서 'books'가 `{prefix}`에 해당
- `{lookup}`: 개별 리소스를 식별하는 값 (주로 'pk' 또는 'id')

###################################
# posts/models.py
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s post - {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.post}"


###################################
# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "created_at", "post"]


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "caption", "image", "created_at", "comments", "likes"]

    def get_likes(self, obj):
        return obj.likes.count()


###################################
# posts > views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        POST 요청을 받았을 때, author 필드에 현재 요청을 보낸 사용자를 넣어줍니다. 이 함수 말고도 perform_update, perform_destroy, perform_list 등이 있습니다.
        '''
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        '''
        /posts/{post_id}/like/ POST 요청을 받았을 때, 좋아요를 생성합니다. 이미 좋아요가 되어있다면 좋아요를 취소합니다.
        '''
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()
            return Response({"status": "unliked"})

        serializer = LikeSerializer(like)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        '''
        /posts/{post_id}/comments/ GET 요청을 받았을 때, 해당 포스트의 댓글을 반환합니다.
        '''
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        '''
        /posts/ GET 요청을 받았을 때, 로그인하지 않은 사용자도 볼 수 있도록 허용합니다. self.action의 주요 액션 타입은 아래와 같습니다.
        - list: 객체 목록 조회 (GET /posts/)
        - retrieve: 단일 객체 조회 (GET /posts/{id}/)
        - create: 객체 생성 (POST /posts/)
        - update: 객체 수정 (PUT /posts/{id}/)
        - partial_update: 객체 일부 수정 (PATCH /posts/{id}/)
        - destroy: 객체 삭제 (DELETE /posts/{id}/)
        '''
        if self.action == "list":
            return [permissions.AllowAny()]
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


###################################
# posts > admin.py

from django.contrib import admin
from .models import Post, Comment, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

###################################

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

###################################

admin에서 게시물 3개 작성
(이미지까지 함께 작성)

###################################
# 썬더클라이언트로 테스트

## 회원 가입(V)
- 메서드: POST
- URL: http://127.0.0.1:8000/accounts/register/
{
  "email": "testuser@example.com",
  "username": "testuser",
  "password": "testpassword123"
}

## 로그인(V)
- 메서드: POST
- URL: http://127.0.0.1:8000/accounts/token/
- 바디:
{
  "email": "testuser@example.com",
  "password": "testpassword123"
}
  
## 프로필 조회(V)
- 메서드: GET
- URL: http://127.0.0.1:8000/accounts/profile/
- 헤더:
  Authorization: Bearer {access_token}

## 게시물 목록 조회(V)
- 메서드: GET
- URL: http://127.0.0.1:8000/posts/

## 단일 게시물 조회(V)
- 메서드: GET
- URL: http://127.0.0.1:8000/posts/1/
- 헤더: 
  Authorization: Bearer {access_token}

## 게시물 생성(V)
- 메서드: POST
- URL: http://127.0.0.1:8000/posts/
- 헤더: 
  Authorization: Bearer {access_token}
- 바디 (form-data):
    "caption": "hello"
    "image": (이미지 파일)

## 게시물 좋아요(V)
- 메서드: POST
- URL: http://127.0.0.1:8000/posts/1/like/
- 헤더: 
  Authorization: Bearer {access_token}


## 댓글 생성(V)
- 메서드: POST
- URL: http://127.0.0.1:8000/posts/comments/
- 헤더: 
  Authorization: Bearer {access_token}
  Content-Type: application/json
- 바디:
  {
    "post": 1,
    "text": "This is a test comment."
  }
  
## 게시물 댓글 조회(V)
- 메서드: GET
- URL: http://127.0.0.1:8000/posts/1/comments/
- 헤더: 
  Authorization: Bearer {access_token}

###################################
# views.py
# @action 데코레이터는 Django REST Framework에서 제공하는 기능으로, ViewSet에 추가적인 엔드포인트를 정의할 때 사용됩니다. 이를 통해 기본 CRUD(Create, Read, Update, Delete) 작업 외에 사용자 정의 액션을 추가할 수 있습니다.
from rest_framework import viewsets
from rest_framework.decorators import action
# 생략

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def sampleone(self, request, pk=None):
        """
        detail=True: 특정 게시물에 대한 작업
        detail=False: 모든 게시물에 대한 작업
        /posts/{pk}/sampleone/: 개별 게시물의 제목과 내용을 반환하는 엔드포인트 (detail=True)
        """
        data = {"title": "hello", "content": "world"}
        return response.Response(data)

    @action(detail=False, methods=["get"])
    def sampletwo(self, request):
        """
        /posts/sampletwo/: 모든 게시물의 제목과 작성자 이름을 반환하는 엔드포인트 (detail=False)
        """
        data = [{"title": "hello 2", "author": "world 2"}]
        return response.Response(data)

###################################
# 아래와 같이 일일이 매서드에 매핑하는 방법도 있습니다.

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from .views import PostViewSet, CommentViewSet

# router = DefaultRouter()
# router.register("posts", PostViewSet)
# router.register("posts/(?P<post_pk>[^/.]+)/comments", CommentViewSet)

# post_list = PostViewSet.as_view({
#     "get": "list",
#     "post": "create"
# })

# post_detail = PostViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy"
# })

# post_sampleone = PostViewSet.as_view({
#     "get": "sampleone"
# })

# post_sampletwo = PostViewSet.as_view({
#     "get": "sampletwo"
# })

# urlpatterns = [
#     path("", include(router.urls)),
#     path("posts/<int:pk>/sampleone/", post_sampleone, name="post-sampleone"),
#     path("posts/sampletwo/", post_sampletwo, name="post-sampletwo"),
# ]

###################################
# views.py
# 아래와 같이 재정의 할 수 있습니다.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return response.Response("Hello, World!")


###################################
# 매서드별 권한 재정의

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        # self.permission_classes = [permissions.AllowAny]
        # self.permission_classes = [permissions.IsAuthenticated]
        return super().list(request, *args, **kwargs)
```