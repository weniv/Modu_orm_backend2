from django.db import models

# 이렇게 이미 만들어진 벨리데이터를 사용할 수도 있습니다.
from django.core.exceptions import ValidationError

# from django.core.validators import MinLengthValidator


def validate_title(value):
    print("models에 validate_title 함수 실행")
    if value == "제주가정말정말좋아":
        # 디버거에서 출력합니다.
        raise ValueError("제주는 좋은 곳입니다!!!")


class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_title])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.title == "제주가정말정말정말좋아":
            # 템플릿에서 출력할 수 있습니다.
            raise ValidationError("제주는 좋은 곳입니다!!!!!")
