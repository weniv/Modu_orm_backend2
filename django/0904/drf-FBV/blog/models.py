from django.db import models
from django.conf import settings


# 여러 곳에서 쓰이면 밖으로 빼서 사용하는 것이 좋습니다.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# settings.py에 AUTH_USER_MODEL 없더라도 기본 값을 사용합니다.
# AUTH_USER_MODEL = 'appname.CustomUser' 형식으로 사용자 모델을 지정할 수 있습니다.


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
