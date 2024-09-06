from rest_framework import serializers
from .models import PostNotice


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNotice
        fields = "__all__"
