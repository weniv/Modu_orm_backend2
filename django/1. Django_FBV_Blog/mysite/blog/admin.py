from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    # 관리자 화면 상단에 출력할 필드를 지정
    list_display = ['title', 'created_date', 'modified_date', 'category']
    # 필터 옵션을 추가 - 특정 필드값에 해당하는 값을 필터링 할 수 있게 옵션 설정
    list_filter = ['created_date', 'category']
    # 검색 옵션을 추가
    search_fields = ['title', 'content']
    # 날짜기반 네비게이션을 추가 - 특정 날짜, 특정 기간에 해당하는 데이터를 탐색
    date_hierarchy = 'created_date'
    # 순서정렬 - (-)를 활용하면 내림차순으로 지정
    ordering = ['-created_date']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
