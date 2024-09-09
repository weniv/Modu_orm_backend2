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
    if created:  # User가 생성되었을 때
        Profile.objects.create(user=instance)
    # 유저가 변경되었을 때
    instance.profile.save()
