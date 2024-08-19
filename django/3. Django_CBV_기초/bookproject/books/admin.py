from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_date'] # 목록에 나타낼 필드 목록
    search_fields = ['title', 'author'] # 검색 기능 추가
    list_filter = ['publication_date'] # 필터 기능 추가