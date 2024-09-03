from django.shortcuts import render
from .models import Post
from django.http import HttpResponse, JsonResponse

# DRF 추가 후 추가된 코드
from rest_framework import views, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# 시리얼라이저 추가
from .serializers import PostSerializer

# CSRF 토큰 추가
from django.middleware.csrf import get_token


# FBV 방식
@api_view(["GET"])
def blog_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    # Response는 기본 Django의 HttpResponse 객체보다 더 많은 기능을 제공합니다.
    # Dict와 같은 것도 자동 변환 해줍니다.
    # 사용자가 원하는 형식으로 자동 변환 해줍니다.
    # 상태 코드도 설정할 수 있습니다.
    # return Response(serializer.data)
    # return Response(100)
    # return Response(100, status=status.HTTP_200_OK)
    # return Response(100, status=404) # 보안상 status를 항상 솔직하게 주지 않는 경우도 있습니다.
    # return Response([10, 20, 30])
    # one = {"name": "one"}
    # two = {"name": "two"}
    # three = {"name": "three"}
    # data = [one, two, three]
    # # 그렇다 하더라도 QuerySet을 직접 넘길 수는 없습니다.
    # return Response(data)
    return Response({"message": "Not Found"}, status=404)


def csrf(request):
    token = get_token(request)
    return JsonResponse({"csrftoken": token})
