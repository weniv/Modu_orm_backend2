from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)
    # 1:N 관계에서 N에 해당하는 Post 모델에 ForeignKey로 User 모델을 연결합니다.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )

    def __str__(self):
        return f"{self.title} | {self.author} | {self.content[:5]}"

    class Meta:
        ordering = ["-created_at"]
