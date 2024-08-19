from django.test import TestCase
from blog.models import Post, Category
from django.utils import timezone

# Create your tests here.

category = Category.objects.create(name = "Python", description = "Python에 대한 모든것")
post = Post.objects.create(title="두번째 블로그", content="나의 두번째 블로그에요", category = category)
print(category, post)