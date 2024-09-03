from rest_framework import serializers
from .models import Post

# 좋은 글: https://velog.io/@jewon119/TIL00.-DRF-ModelViewSet-%EA%B0%84%EB%8B%A8-%EC%82%AC%EC%9A%A9%EA%B8%B0


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
