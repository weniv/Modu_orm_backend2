```python
###################################
쉘에서 데이터 수정, 삭제(V)
Q 객체(V)
###################################
템플릿 필터 명령어 정리(V)
###################################
유효성 검사
    - Front-end에 유효성 검사
    - Django Forms에 유효성 검사
    - Django Views에 유효성 검사
    - Django Models에 유효성 검사
###################################
tailwind
###################################

mkdir qna
cd qna
python -m venv venv
.\venv\Scripts\activate
pip install django
django-admin startproject config .
python manage.py migrate

###################################

python manage.py startapp main

###################################

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

###################################
# config/urls.py

from django.contrib import admin
from django.urls import path
from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]

###################################
# main/views.py

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the main index.")


###################################
# main/models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

###################################

python manage.py makemigrations
python manage.py migrate

###################################

from django.contrib import admin
from .models import Post

admin.site.register(Post)

###################################

python manage.py createsuperuser
leehojun
leehojun@gmail.com
dlghwns1234!

###################################

python manage.py runserver

게시물 4개 등록

1 11 111
2 22 222
3 33 333
11 123 123

###################################

python manage.py shell

###################################

python manage.py shell


>>> from main.models import Post
>>> Post.objects.all()
<QuerySet [<Post: 1>, <Post: 2>, <Post: 3>, <Post: 11>]>
>>> data = Post.objects.all()
>>> type(data)
<class 'django.db.models.query.QuerySet'>
>>> data[0] 
<Post: 1>
>>> type(data[0])
<class 'main.models.Post'>
>>> data[0].title
'1'
>>> data[0].content
'11'
>>> dir(data)
['__aiter__', '__and__', '__bool__', '__class__', '__class_getitem__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', 
'__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '__xor__', '_add_hints', '_annotate', '_batched_insert', 
'_chain', '_check_bulk_create_options', '_check_operator_queryset', '_check_ordering_first_last_queryset_aggregation', '_clone', '_combinator_query', '_db', '_defer_next_filter', '_deferred_filter', '_earliest', '_extract_model_params', '_fetch_all', '_fields', '_filter_or_exclude', '_filter_or_exclude_inplace', '_for_write', '_has_filters', '_hints', '_insert', '_iterable_class', '_iterator', '_known_related_objects', '_merge_known_related_objects', '_merge_sanity_check', '_next_is_sticky', '_not_support_combined_queries', '_prefetch_done', '_prefetch_related_lookups', '_prefetch_related_objects', '_prepare_for_bulk_create', '_query', '_raw_delete', '_result_cache', '_sticky_filter', '_update', '_validate_values_are_expressions', '_values', 'aaggregate', 'abulk_create', 'abulk_update', 'acontains', 'acount', 'acreate', 'adelete', 'aearliest', 'aexists', 'aexplain', 'afirst', 'aget', 'aget_or_create', 'aggregate', 'ain_bulk', 'aiterator', 'alast', 'alatest', 'alias', 'all', 'annotate', 'as_manager', 'aupdate', 'aupdate_or_create', 'bulk_create', 'bulk_update', 'complex_filter', 'contains', 'count', 'create', 'dates', 'datetimes', 'db', 'defer', 'delete', 'difference', 'distinct', 'earliest', 'exclude', 'exists', 'explain', 'extra', 'filter', 'first', 'get', 'get_or_create', 'in_bulk', 'intersection', 'iterator', 'last', 'latest', 'model', 'none', 'only', 'order_by', 'ordered', 'prefetch_related', 'query', 'raw', 'resolve_expression', 'reverse', 'select_for_update', 'select_related', 'union', 'update', 'update_or_create', 'using', 'values', 'values_list']
# Read
>>> Post.objects.all()              
<QuerySet [<Post: 1>, <Post: 2>, <Post: 3>, <Post: 11>]>
>>> Post.objects.all().order_by('-pk')
<QuerySet [<Post: 11>, <Post: 3>, <Post: 2>, <Post: 1>]>
>>> Post.objects.count()
4
>>> Post.objects.get(id=1) 
<Post: 1>
>>> one = Post.objects.get(id=1)
>>> one['title']
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: 'Post' object is not subscriptable
>>> one.title   
'1'
>>> q = Post.objects.get(id=1)
>>> q.id
1
>>> q.pk
1
>>> q.title
'1'
>>> q.content
'11'
>>> q.created_at
datetime.datetime(2024, 8, 20, 3, 43, 28, 312330, tzinfo=datetime.timezone.utc)
>>> Post.objects.filter(title='1')
<QuerySet [<Post: 1>]>
>>> Post.objects.filter(title='11') 
<QuerySet [<Post: 11>]>
>>> Post.objects.filter(id=1)       
<QuerySet [<Post: 1>]>
>>> Post.objects.filter(title__contains='1')  
<QuerySet [<Post: 1>, <Post: 11>]>
>>> q = Post.objects.filter(title__contains='1')   
>>> type(q)
<class 'django.db.models.query.QuerySet'>
>>> q.filter(id=1).filter(content__contains='1') 
<QuerySet [<Post: 1>]>
>>> Post.objects.filter(id=1).filter(content__contains='1').filter(title__contains='1')
<QuerySet [<Post: 1>]>
>>> Post.objects.filter(id__lt=2) 
<QuerySet [<Post: 1>]>
>>> Post.objects.filter(id__lt=3) 
<QuerySet [<Post: 1>, <Post: 2>]>
>>> Post.objects.filter(id__lt=3) #little라고 외우지만 Less than
<QuerySet [<Post: 1>, <Post: 2>]>
>>> Post.objects.filter(id__gt=3) #greater라고 외우지만 Greater than
<QuerySet [<Post: 11>]>


eq - equal ( = )
ne - not equal ( <> )
lt - little(Less than) ( < )
le - little or equal ( <= )
gt - greater(Greater than) ( > )
ge - greater or equal ( >= )

# Create
# 내부적으로 create() 메서드는 save()를 호출하여 객체를 데이터베이스에 저장
# 따라서 Create을 할 때에는 save()를 호출하지 않아도 된다.
# save()가 필요한 경우: 기존 객체를 수정할 때
>>> q = Post.objects.create(title='t1', content='t11', tag='t123')
>>> q
<Post: t1>
>>> Post.objects.all()
<QuerySet [<Post: 1>, <Post: 2>, <Post: 3>, <Post: 11>, <Post: t1>]>
>>> q.created_at
datetime.datetime(2024, 8, 20, 5, 34, 40, 357881, tzinfo=datetime.timezone.utc)
>>> q.save()
>>> Post.objects.all()
<QuerySet [<Post: 1>, <Post: 2>, <Post: 3>, <Post: 11>, <Post: t1>]>
>>> q = Post.objects.create(title='t2')                            
>>> q.save()          
>>> q.content
''

# Delete
>>> q = Post.objects.get(id=1)
>>> q.delete()
(1, {'main.Post': 1})
>>> Post.objects.all()
<QuerySet [<Post: 2>, <Post: 3>, <Post: 11>, <Post: t1>, <Post: t2>]>

# Update
>>> q = Post.objects.get(id=2)
>>> q.title = 'hello world' 
>>> q
<Post: hello world>
>>> Post.objects.all()
<QuerySet [<Post: 2>, <Post: 3>, <Post: 11>, <Post: t1>, <Post: t2>]>
>>> q.save()
>>> Post.objects.all()[:3]
<QuerySet [<Post: hello world>, <Post: 3>, <Post: 11>]>

###################################
posts = Post.objects.all()

1. 연도와 일치되는 게시물 가져오기
posts = Post.objects.filter(created_at__year=2024)

2. 월과 일치되는 게시물 가져오기
posts = Post.objects.filter(created_at__month=2)

3. 일과 일치되는 게시물 가져오기
posts = Post.objects.filter(created_at__day=28)

4. 월과 일에 일치되는 게시물 가져오기
posts = Post.objects.filter(created_at__month=2, created_at__day=28)

5. 연, 월, 일에 매칭이 되는 게시물 가져오기
gt (greater than) : >
lt (less than) : <
gte (greater than or equal) : >=
lte (less than or equal) : <=

from datetime import date

posts = Post.objects.filter(created_at__gte=date(2023,10,17))


###################################
# Q 객체
# Q 객체는 속도 향상을 위해 사용하지는 않습니다. 가독성을 위해 가장 많이 사용합니다.
# filter.filter.filter 속도 차이가 나지 않습니다.
# 다만 복잡한 쿼리에 있어서 filter.filter.filter에 조합으로 조합이 어렵거나, 가독성이 떨어지거나, 속도가 차이가 나는 경우 Q객체를 많이 사용합니다.
# filter는 결국 and만 사용할 수 있습니다.
# Q 객체는 and, or, not을 사용할 수 있습니다.

>>> from django.db.models import Q
>>> Post.objects.filter(~Q(title__contains='1'))                          
<QuerySet [<Post: hello world>, <Post: 3>, <Post: t2>]>
>>> Post.objects.filter(~Q(title__contains='1') & Q(title__contains='2')) 
<QuerySet [<Post: t2>]>


###################################
# 템플릿 필터 명령어 정리

# main > views.py
from django.shortcuts import render
from .models import Post


def index(request):
    post = Post.objects.get(pk=2)  # 아까 delete해서 pk=1이 없어져서 pk=2로 변경
    return render(request, "main/index.html", {"post": post})

###################################
# main > templates > main > index.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <title>템플릿 필터 명령어</title>
</head>
<body>
    <!-- title: hello world -->
    <!-- content: 22 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam id arcu sed risus malesuada venenatis. Aliquam in mattis neque, ac dictum massa. Fusce volutpat elit odio. 

    Praesent iaculis lectus eu pellentesque consequat. Donec nec efficitur leo. 

    Quisque ac malesuada enim, nec maximus justo. Sed ac facilisis mauris.

    <h1>hello world</h1> -->

    <p>{{ post.title }}</p>
    <p>{{ post.content }}</p>
    <p>{{ post.content | upper }}</p>
    <p>{{ post.content | lower }}</p>
    <p>(V) {{ post.content | linebreaks }}</p>
    <p>(V) 말줄임: {{ post.content | truncatewords:5 }}</p>
    <p>말줄임: {{ post.content | truncatewords:7 }}</p>
    <p>슬라이싱: {{ post.content | slice:":10" }}</p>
    <p>공백 병합(join): {{ post.content | join:'-' }}</p>
    <p>['hello', 'world', 'hi'] => hello-world-hi</p>
    <p>(V) 길이: {{ post.content | length }}</p>
    <p>태그 없애기: {{ post.content | striptags }}</p>
    <p>문자열에 더하기: {{ post.content | add:"!" }}</p>
    <p>날짜: {{ post.created_at }}</p>
    <p>(V) 날짜 형식 바꾸기: {{ post.created_at | date:"y/m/d" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"y-m-d" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"y" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"Y" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"M" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"D" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"h" }}</p>
    <p>날짜 형식 바꾸기: {{ post.created_at | date:"i" }}</p>
    <p>필터 중첩: {{ post.content | upper | linebreaks | truncatewords:10 }}</p>

{% lorem 2 p %}

<!-- 저는 잘 사용하진 않습니다. -->
{% lorem 1 b random %}
{% lorem 1 p random %}
{% lorem 2 w random %}
<!-- 단어 w, 단락 p, 일반텍스트 b -->
{# lorem [count] [method] [random] #}

<!-- 사용하지 마세요. -->
{% autoescape off %}
{{ post.content }}
{% endautoescape %}
</body>
</html>

###################################
# 실습 안하는 코드

{% for i in posts %}
    <h1>{{ i.title }}</h1>
    <p>{{ i.content }}</p>
    <p>{{ forloop.counter }}</p>
    <p>{{ forloop.counter0 }}</p>
    <p>{{ forloop.counter|add:100 }}</p>
    <p>{{ forloop.revcounter }}</p>
    <p>{{ forloop.first }}</p>
    <p>{{ forloop.last }}</p>
    <hr>
{% endfor %}

###################################
# 실습 안하는 코드

{# 자주 사용하지 않습니다. #}
{% with value='hello world' %}
    <h1>{{value}}</h1>
{% endwith %}

###################################
# 실습 안하는 코드

{# 주석입니다. #}
{% comment 'licat' %}
이 코드는 영국에서 시작되어...
{% endcomment %}
hello world

###################################
# 실습 안하는 코드

{# 실습 안합니다. #}
{% url 'some-url-name' v1 v2 %}
{% url 'some-url-name' arg1=v1 arg2=v2 %}

path("client/<int:id>/", app_views.client, name="app-views-client")
{% url 'app-views-client' client.id %}

###################################
# 실습 안하는 코드

# django의 이스케이프 기능 비활성화하는 법 2가지(특수한 경우에만 사용합니다. 이 코드는 위험합니다.)
{% for i in posts %}
    <p>{{i.content|safe}}</p>
{% endfor %}

<hr>

{% for i in posts %}
    {% autoescape off %}
    <p>{{i.content}}</p>
    {% endautoescape %}
{% endfor %}

###################################
# markdown, 많이 사용합니다.
# django-markdown은 만든 사람이 많습니다.
# 제가 사용한 모듈이 비교를 해봤을 때 가장 단순하게 사용할 수 있습니다.

# pip install django-markdown-deux
# settings.py 'markdown_deux'(마크다운 두) 등록
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 서드파티
    "markdown_deux",
    # 커스텀
    "blog",
]

###################################

python manage.py runserver

###################################
# blog_list.html
{% load markdown_deux_tags %}
{% for i in posts %}
    <p>{{ i.content | markdown }}</p>
{% endfor %}

# 8번 게시물로 작성합니다.
# hello world
## hello world
### hello world

1. hello world
2. hello world

* hello world
* hello world
* hello world

{{'# hello world' | markdown }}

###################################


질문: html의 클래스는 어떻게 주나요?

1. 아래처럼 주는 방법이 있습니다.
<form method="POST">
{% csrf_token %}
{{form.title}}
{{form.content}}
<button type="submit">제출</button>
</form>

<form method="POST">
{% csrf_token %}
<input type="text" name="title" class="클래스" value="{{ form.title.value|default:'' }}">
<input type="text" name="content" class="클래스" value="{{ form.content.value|default:'' }}">
<button type="submit">제출</button>
</form>


2. django 위젯을 깔아 하는 방법이 있습니다.
https://pypi.org/project/django-widget-tweaks/

{% load widget_tweaks %}
<form method="POST">
{% csrf_token %}
{{ form.title|add_class:"클래스" }}
{{ form.content|add_class:"클래스" }}
</form>
```