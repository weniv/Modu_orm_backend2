```python
mkdir serializers
cd serializers
python -m venv venv
# source venv/Scripts/activate
.\venv\Scripts\activate
pip install django djangorestframework pillow
django-admin startproject config .
python manage.py startapp blog

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
    "blog",
]

# 중략..

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"


###################################
# blog > models.py

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    caption = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption


###################################
# blog > serializers.py

from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    testdata = serializers.SerializerMethodField()

    # 모델에는 없는 필드를 만드는 방법은 명시적인 방법과 암시적인 방법이 있습니다.
    # 위 방법은 명시적인 방법입니다.
    # 이러한 방식을 사용했을 때에는 여러 파리터를 사용할 수 있습니다.

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "caption",
            "created_at",
            "author_username",
            "testdata",
        ]

    def get_author_username(self, obj):
        return obj.author.username

    def get_testdata(self, obj):
        return "test!!"


###################################
# blog > views.py

from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

###################################
# config > urls.py
from django.urls import path
from blog.views import PostListCreateView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
]

###################################

python manage.py makemigrations
python manage.py migrate

###################################
# blog > admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

###################################

python manage.py createsuperuser

###################################

python manage.py runserver

# 게시물 3개 작성

###################################
# thunder client

GET http://127.0.0.1:8000/posts/

###################################
# serializers 테스트

from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    testdata = serializers.SerializerMethodField()
    testdata2 = serializers.SerializerMethodField()
    testdata3 = serializers.SerializerMethodField()

    # 모델에는 없는 필드를 만드는 방법은 명시적인 방법과 암시적인 방법이 있습니다.
    # 위 방법은 명시적인 방법입니다.
    # 이러한 방식을 사용했을 때에는 여러 파리터를 사용할 수 있습니다.

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "caption",
            "created_at",
            "author_username",
            "testdata",
            "testdata2",
            "testdata3",
        ]

    def get_author_username(self, obj):
        return obj.author.username

    def get_testdata(self, obj):
        return "test!!"

    def get_testdata2(self, obj):
        # obj가 Post가 맞는지 확인하는 작업일 뿐입니다.
        value = f"<--{obj.caption}-->"
        return value

    def get_testdata3(self, obj):
        return len(obj.caption)


###################################
# serializers 고도화
# models.py 수정

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


###################################

from rest_framework import serializers
from .models import Comment, Post, Like

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author']

    def get_author_username(self, obj):
        # 이 메소드는 'author_username' 필드의 값을 생성합니다.
        # obj는 현재 처리 중인 Comment 인스턴스입니다.
        # 필드 이름이 'author_username'이면 'get_필드명' 형식의 메소드를 호출하여 값을 생성합니다.
        # 이 필드는 실제 Comment 모델에는 없지만, 이 필드를 통해 댓글 작성자의 사용자 이름을 반환합니다.
        return obj.author.username  # 댓글 작성자의 사용자 이름을 반환합니다.

    def create(self, validated_data):
        # 시리얼라이저에서 .save() 메소드를 호출할 때 실행됩니다.
        # 댓글 생성 시 현재 인증된 사용자를 작성자로 설정합니다.
        # self.context['request']를 통해 현재 요청 객체에 접근할 수 있습니다.
        validated_data['author'] = self.context['request'].user
        # 부모 클래스의 create 메소드를 호출하여 댓글을 생성합니다.
        return super().create(validated_data)

# 예를 들어 create은 아래와 같은 형태에서 
# class BookListCreateView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() # 이 부분에서 작동하게 됩니다.
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField() # 명시적 방법입니다. 없으면 암시적으로 작동합니다. 명시적으로 작성할 경우 파라미터 값을 지정할 수 있습니다.
    comments = CommentSerializer(many=True, read_only=True)
    likesCount = serializers.IntegerField(source='likes.count', read_only=True)
    isLiked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'caption', 'created_at', 'comments', 'likesCount', 'isLiked']
        read_only_fields = ['author']

    def get_isLiked(self, obj):
        # 현재 사용자가 이 게시물에 좋아요를 눌렀는지 확인합니다.
        user = self.context['request'].user
        if user.is_authenticated:
            # Like 모델을 사용하여 현재 사용자가 게시물에 좋아요를 눌렀는지 확인합니다.
            return Like.objects.filter(post=obj, user=user).exists()
        return False
    
    def get_author_username(self, obj):
        # 게시물 작성자의 사용자 이름을 반환합니다.
        return obj.author.username

    def create(self, validated_data):
        # 게시물 생성 시 현재 인증된 사용자를 작성자로 설정합니다.
        validated_data['author'] = self.context['request'].user
        print(validated_data['author'])
        print(validated_data)
        print(self.context['request'])
        return super().create(validated_data)


##############################################

python manage.py makemigrations
python manage.py migrate

##############################################
# thunder client
# thunder client로 collection 생성 후 작성한 다음 export한 내용
# collection으로 run 실행

# GET http://127.0.0.1:8000/posts/
# POST http://127.0.0.1:8000/posts/
auth: basic
body: form
    - caption: 33
    - file을 체크하시면 파일도 포함시킬 수 있습니다.
# GET http://127.0.0.1:8000/posts/1/

###################################
{
    "clientName": "Thunder Client",
    "collectionName": "a",
    "collectionId": "7ce54275-58f1-4f4e-8cb3-675d4c85b39d",
    "dateExported": "2024-09-05T14:29:16.960Z",
    "version": "1.2",
    "folders": [],
    "requests": [
        {
            "_id": "998cce36-a802-4b00-a3af-31be85e19070",
            "colId": "7ce54275-58f1-4f4e-8cb3-675d4c85b39d",
            "containerId": "",
            "name": "http://127.0.0.1:8000/posts/",
            "url": "http://127.0.0.1:8000/posts/",
            "method": "POST",
            "sortNum": 10000,
            "created": "2024-09-05T14:29:11.074Z",
            "modified": "2024-09-05T14:29:11.074Z",
            "headers": [],
            "body": {
                "type": "formdata",
                "raw": "",
                "form": [
                    {
                        "name": "caption",
                        "value": "33"
                    },
                    {
                        "name": "author",
                        "value": "1"
                    }
                ],
                "files": [
                    {
                        "name": "image",
                        "value": "c:\\Users\\paullab\\Desktop\\2024.png"
                    }
                ]
            },
            "auth": {
                "type": "basic",
                "basic": {
                    "username": "leehojun",
                    "password": "dlghwns1234!"
                }
            }
        }
    ],
    "ref": "2C_JFYQjc15koxi98PAaIZqBssULn_wi1fzL9Eg0V7ANFdtjYhJ1dUJoPC7cI-BIKfYbj_AWEYmTA_W20sz0fQ"
}