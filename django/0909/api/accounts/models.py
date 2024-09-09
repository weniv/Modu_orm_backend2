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
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        슈퍼유저 생성 메서드입니다. is_staff와 is_superuser는 True로 설정됩니다. 오버라이드하여 변경할 수 있습니다.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
