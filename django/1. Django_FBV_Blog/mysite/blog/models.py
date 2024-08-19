from django.db import models
from django.utils import timezone 
# Create your models here.

# 네이버 블로그
# 카테고리를 IT/컴퓨터로 설정하고, 포스트를 작성하면, 해당 카테고리에 포스트가 저장되는 형태

# 카테고리 모델 클래스 생성
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) # blank=True는 필수가 아님을 의미함
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories' # 복수형 이름을 지정함

# Post 모델을 정의 - 데이터베이스에 저장될 테이블을 정의
class Post(models.Model):
    title = models.CharField(max_length=200) # max값을 지정해야할때
    content = models.TextField() # 길이 제한이 없을때
    created_date = models.DateTimeField(default=timezone.now) # 날짜와 시간을 의미함
    modified_date = models.DateTimeField(auto_now=True) # 수정될때마다 시간이 자동으로 업데이트됨
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        null=True, 
        related_name = 'posts'
    ) # Category 모델과 Post 모델을 1:N 관계로 연결함
    # ForeignKey는 다른 모델과의 관계를 정의함 1:N 관계를 정의할때 사용함
    # 카테고리는 1개 포스트는 여러개를 쓸수 있는 구조!
    # CASCADE - 부모 객체가 삭제되면 이에 연결된 자식 객체도 삭제됨
    # 1:1(일대일) OneToOneField, N:N(다대다)관계는 ManyToManyField를 사용함
    
    class Meta:
        ordering = ['-created_date'] # -가 있으면 내림차순, 없으면 오름차순

    def __str__(self):
        return self.title