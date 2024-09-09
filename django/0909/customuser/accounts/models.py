# models.py
# \venv\Lib\site-packages\django\contrib\auth\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # 기존 User 모델의 필드들을 모두 상속받습니다.
    # 추가로 원하는 필드를 정의할 수 있습니다.
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # 이 부분은 선택사항입니다. USERNAME_FIELD를 변경하고 싶다면 아래와 같이 설정할 수 있습니다.
    # USERNAME_FIELD = 'email'  # 이메일을 사용자 식별자로 사용하고 싶을 때
    # REQUIRED_FIELDS = ['username']  # createsuperuser 명령어 실행 시 요구되는 필드

    def __str__(self):
        return self.username
