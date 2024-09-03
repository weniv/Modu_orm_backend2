from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from .serializers import PostSerializer
from rest_framework import status
from .models import Post


@extend_schema(
    summary="Blog list",
    description="모든 블로그 포스트의 목록을 가져옵니다.",
    parameters=[
        OpenApiParameter(
            name="title", description="제목으로 필터링", required=True, type=str
        )
    ],
    responses={
        200: OpenApiResponse(
            response=PostSerializer(many=True),
            description="성공적으로 포스트 목록을 가져왔습니다.",
        ),
        400: OpenApiResponse(description="잘못된 요청"),
    },
    examples=[
        OpenApiExample(
            "Response example",
            value=[
                {
                    "id": 1,
                    "title": "첫 번째 포스트",
                    "content": "이것은 첫 번째 포스트의 내용입니다.",
                },
                {
                    "id": 2,
                    "title": "두 번째 포스트",
                    "content": "이것은 두 번째 포스트의 내용입니다.",
                },
            ],
            response_only=True,
        )
    ],
)
@api_view(["GET"])
def blog_list(request):
    title = request.query_params.get("title")
    created_after = request.query_params.get("created_after")

    posts = Post.objects.all()

    if title:
        posts = posts.filter(title__icontains=title)

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Post detail operations",
    description="특정 포스트에 대한 상세 조회, 수정, 삭제 작업을 수행합니다.",
    request=PostSerializer,
    responses={
        200: OpenApiResponse(
            response=PostSerializer,
            description="성공적으로 포스트를 조회/수정했습니다.",
        ),
        204: OpenApiResponse(description="성공적으로 포스트를 삭제했습니다."),
        400: OpenApiResponse(description="잘못된 요청"),
        404: OpenApiResponse(description="포스트를 찾을 수 없습니다."),
    },
    examples=[
        OpenApiExample(
            "Valid input example",
            value={"title": "수정된 제목", "content": "이것은 수정된 내용입니다."},
            request_only=True,
        ),
        OpenApiExample(
            "Response example",
            value={
                "id": 1,
                "title": "수정된 제목",
                "content": "이것은 수정된 내용입니다.",
            },
            response_only=True,
        ),
        OpenApiExample(
            "JavaScript fetch examples",
            value={
                "x-code-samples": [
                    {
                        "lang": "JavaScript (GET)",
                        "source": """
fetch('http://api.example.com/blog/1')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
""",
                    },
                    {
                        "lang": "JavaScript (PUT)",
                        "source": """
fetch('http://api.example.com/blog/1', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: '수정된 제목',
    content: '이것은 수정된 내용입니다.'
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
""",
                    },
                    {
                        "lang": "JavaScript (DELETE)",
                        "source": """
fetch('http://api.example.com/blog/1', {
  method: 'DELETE'
})
.then(response => {
  if(response.status === 204) {
    console.log('Post deleted successfully');
  }
})
.catch(error => console.error('Error:', error));
""",
                    },
                ]
            },
            request_only=True,
        ),
    ],
)
@api_view(["GET", "PUT", "DELETE"])
def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
