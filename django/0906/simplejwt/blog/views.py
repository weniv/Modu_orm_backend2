from rest_framework.views import APIView
from rest_framework.response import Response

# 이 인증은 원래 simplejwt로 하는 것이 아니라, django rest framework에서 제공하는 인증 방식이었으나
# 우리가 settings.py에서 설정을 해주었기 때문에 simplejwt로 인증을 하는 것이다.
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
