from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # UserAdmin을 상속받아 커스텀 필드를 관리자 페이지에 표시합니다.
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("bio", "birth_date")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
