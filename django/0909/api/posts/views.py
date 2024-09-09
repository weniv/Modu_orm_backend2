from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        POST 요청을 받았을 때, author 필드에 현재 요청을 보낸 사용자를 넣어줍니다. 이 함수 말고도 perform_update, perform_destroy, perform_list 등이 있습니다.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        """
        /posts/{post_id}/like/ POST 요청을 받았을 때, 좋아요를 생성합니다. 이미 좋아요가 되어있다면 좋아요를 취소합니다.
        """
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()
            return Response({"status": "unliked"})

        serializer = LikeSerializer(like)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        """
        /posts/{post_id}/comments/ GET 요청을 받았을 때, 해당 포스트의 댓글을 반환합니다.
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """
        /posts/ GET 요청을 받았을 때, 로그인하지 않은 사용자도 볼 수 있도록 허용합니다. self.action의 주요 액션 타입은 아래와 같습니다.
        - list: 객체 목록 조회 (GET /posts/)
        - retrieve: 단일 객체 조회 (GET /posts/{id}/)
        - create: 객체 생성 (POST /posts/)
        - update: 객체 수정 (PUT /posts/{id}/)
        - partial_update: 객체 일부 수정 (PATCH /posts/{id}/)
        - destroy: 객체 삭제 (DELETE /posts/{id}/)
        """
        if self.action == "list":
            return [permissions.AllowAny()]
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
